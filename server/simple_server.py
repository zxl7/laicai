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
    req = Request(url, headers={"Referer": "https://finance.sina.com.cn/"})
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

