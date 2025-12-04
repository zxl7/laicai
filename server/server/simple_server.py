import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen

def _normalize_symbol(symbol: str) -> str:
    s = symbol.strip().lower()
    m = re.match(r"^(sh|sz)\d{6}$", s)
    if m:
        return s
    m = re.match(r"^(\d{6})$", s)
    if m:
        code = m.group(1)
        prefix = "sh" if code.startswith("6") or code.startswith("9") else "sz"
        return f"{prefix}{code}"
    raise ValueError("symbol格式不正确")

def _symbol_to_instrument(symbol: str) -> str:
    s = symbol.strip().lower()
    m = re.match(r"^(sh|sz)(\d{6})$", s)
    if m:
        exch = m.group(1).upper()
        code = m.group(2)
        return f"{code}.{exch}"
    m = re.match(r"^(\d{6})$", s)
    if m:
        code = m.group(1)
        exch = "SH" if code.startswith("6") or code.startswith("9") else "SZ"
        return f"{code}.{exch}"
    m = re.match(r"^(\d{6})\.(sh|sz)$", s)
    if m:
        return f"{m.group(1)}.{m.group(2).upper()}"
    raise ValueError("symbol格式不正确")

def _round_price(v: float) -> float:
    return float(f"{v:.2f}")

def _limit_rate(code: str, name: str) -> float:
    n = name.upper()
    if n.startswith("*ST") or n.startswith("ST"):
        return 0.05
    if code.startswith("300") or code.startswith("301") or code.startswith("688"):
        return 0.20
    return 0.10

def _fetch_sina(sym: str) -> dict:
    url = "http://hq.sinajs.cn/list=" + sym
    req = Request(url, headers={
        "Referer": "https://finance.sina.com.cn/",
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/plain, */*;q=0.1",
        "Connection": "keep-alive",
    })
    with urlopen(req, timeout=5) as resp:
        if resp.status != 200:
            raise ValueError("行情接口请求失败")
        txt = resp.read().decode("utf-8", errors="ignore")
    m = re.search(r'"([^"]*)"\s*;', txt)
    if not m:
        raise ValueError("未获取到行情数据")
    parts = m.group(1).split(",")
    if len(parts) < 32:
        raise ValueError("行情数据格式错误")
    name = parts[0]
    open_price = float(parts[1]) if parts[1] else 0.0
    prev_close = float(parts[2]) if parts[2] else open_price
    price = float(parts[3]) if parts[3] else prev_close
    high = float(parts[4]) if parts[4] else price
    low = float(parts[5]) if parts[5] else price
    dt = parts[30] + " " + parts[31]
    change_amount = price - prev_close
    change_percent = (change_amount / prev_close * 100) if prev_close else 0.0
    code = sym[2:]
    return {
        "code": code,
        "name": name,
        "price": _round_price(price),
        "change_percent": _round_price(change_percent),
        "change_amount": _round_price(change_amount),
        "open": _round_price(open_price),
        "high": _round_price(high),
        "low": _round_price(low),
        "prev_close": _round_price(prev_close),
        "time": dt,
    }

def _fetch_third_party(symbol: str) -> dict:
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = os.environ.get("THIRD_PARTY_API_KEY")
    if not base:
        return _fetch_sina(_normalize_symbol(symbol))
    if "biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument"):
        return _fetch_sina(_normalize_symbol(symbol))
    qs = f"symbol={symbol}"
    if api_key:
        qs += f"&api_key={api_key}"
    url = base.rstrip("/") + "/quote?" + qs
    req = Request(url)
    with urlopen(req, timeout=10) as resp:
        if resp.status != 200:
            raise ValueError("第三方接口请求失败")
        data = json.loads(resp.read().decode("utf-8", errors="ignore"))
    if not isinstance(data, dict):
        raise ValueError("第三方接口返回格式错误")
    required = ["code", "name", "price", "prev_close", "open", "high", "low", "time"]
    if all(k in data for k in required):
        price = float(data["price"]) if data["price"] is not None else 0.0
        prev_close = float(data["prev_close"]) if data["prev_close"] is not None else price
        change_amount = price - prev_close
        change_percent = (change_amount / prev_close * 100) if prev_close else 0.0
        return {
            "code": str(data["code"]),
            "name": str(data["name"]),
            "price": _round_price(price),
            "change_percent": _round_price(change_percent),
            "change_amount": _round_price(change_amount),
            "open": _round_price(float(data["open"])) if data["open"] is not None else _round_price(price),
            "high": _round_price(float(data["high"])) if data["high"] is not None else _round_price(price),
            "low": _round_price(float(data["low"])) if data["low"] is not None else _round_price(price),
            "prev_close": _round_price(prev_close),
            "time": str(data["time"]),
        }
    return _fetch_sina(_normalize_symbol(symbol))

def get_quote(symbol: str) -> dict:
    return _fetch_third_party(symbol)

def get_limit_status(symbol: str) -> dict:
    base = os.environ.get("THIRD_PARTY_BASE_URL")
    api_key = os.environ.get("THIRD_PARTY_API_KEY")
    if base and ("biyingapi.com" in base or base.rstrip("/").endswith("/hsstock/instrument")):
        try:
            instrument = _symbol_to_instrument(symbol)
            url = base.rstrip("/") + "/" + instrument + ("/" + api_key if api_key else "")
            req = Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, */*;q=0.1",
                "Connection": "keep-alive",
                "Referer": "https://api.biyingapi.com/",
            })
            with urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    raise ValueError("第三方接口请求失败")
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if not isinstance(data, dict):
                raise ValueError("第三方接口返回格式错误")
            code_tp = str(data.get("ii") or "")
            name_tp = str(data.get("name") or "")
            prev_close = float(data.get("pc") or 0.0)
            up = float(data.get("up") or 0.0)
            down = float(data.get("dp") or 0.0)
            sina = _fetch_sina(_normalize_symbol(symbol))
            price = sina.get("price", 0.0)
            is_flag = int(data.get("is") or 0)
            is_up = bool(is_flag == 1 or (price >= up - 1e-6))
            is_down = bool(is_flag == -1 or (price <= down + 1e-6))
            rate = 0.0
            if prev_close:
                rate = _round_price((up / prev_close) - 1.0) if up else _limit_rate(code_tp or sina.get("code", ""), name_tp or sina.get("name", ""))
            return {
                "code": code_tp or sina.get("code", ""),
                "name": name_tp or sina.get("name", ""),
                "price": price,
                "limit_up_price": _round_price(up) if up else _round_price(prev_close * (1 + rate)),
                "limit_down_price": _round_price(down) if down else _round_price(prev_close * (1 - rate)),
                "is_limit_up": bool(is_up),
                "is_limit_down": bool(is_down),
                "limit_rate": _round_price(rate if rate else _limit_rate(code_tp or sina.get("code", ""), name_tp or sina.get("name", ""))),
            }
        except Exception:
            pass
    q = get_quote(symbol)
    rate = _limit_rate(q["code"], q["name"])
    up = _round_price(q["prev_close"] * (1 + rate))
    down = _round_price(q["prev_close"] * (1 - rate))
    is_up = q["price"] >= up - 1e-6
    is_down = q["price"] <= down + 1e-6
    return {
        "code": q["code"],
        "name": q["name"],
        "price": q["price"],
        "limit_up_price": up,
        "limit_down_price": down,
        "is_limit_up": bool(is_up),
        "is_limit_down": bool(is_down),
        "limit_rate": rate,
    }

class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            self._json(200, {"service": "laicai-stock", "endpoints": ["/quote", "/limit-status"]})
            return
        if url.path == "/quote":
            params = parse_qs(url.query)
            symbol = params.get("symbol", [None])[0]
            if not symbol:
                self._json(400, {"error": "缺少symbol参数"})
                return
            try:
                data = get_quote(symbol)
                self._json(200, data)
            except Exception as e:
                self._json(400, {"error": str(e)})
            return
        if url.path == "/limit-status":
            params = parse_qs(url.query)
            symbol = params.get("symbol", [None])[0]
            if not symbol:
                self._json(400, {"error": "缺少symbol参数"})
                return
            try:
                data = get_limit_status(symbol)
                self._json(200, data)
            except Exception as e:
                self._json(400, {"error": str(e)})
            return
        self._json(404, {"error": "Not Found"})

def main():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
