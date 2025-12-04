import os
import requests
import time
from typing import Dict, Any, List, Optional

from ..common.utils import round_price, format_hms, read_env_from_file


def get_limit_up_pool(date: Optional[str] = None) -> List[Dict[str, Any]]:
    base = os.environ.get("THIRD_PARTY_ZTGC_BASE_URL") or "https://api.biyingapi.com/hslt/ztgc"
    api_key = os.environ.get("THIRD_PARTY_API_KEY") or read_env_from_file("THIRD_PARTY_API_KEY")
    if not api_key:
        try:
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("THIRD_PARTY_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                            break
        except Exception:
            pass
    if not api_key:
        raise ValueError("缺少第三方licence(THIRD_PARTY_API_KEY)")
    if not date:
        date = time.strftime("%Y-%m-%d", time.localtime())
    url = base.rstrip("/") + "/" + date + "/" + api_key
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, */*;q=0.1",
        "Connection": "keep-alive",
        "Referer": "https://api.biyingapi.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ValueError("涨停股池接口请求失败")
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("涨停股池返回格式错误")
    items: List[Dict[str, Any]] = []
    for it in data:
        items.append({
            "code": str(it.get("dm") or ""),
            "name": str(it.get("mc") or ""),
            "price": round_price(float(it.get("p") or 0.0)),
            "change_percent": round_price(float(it.get("zf") or 0.0)),
            "amount": round_price(float(it.get("cje") or 0.0)),
            "float_market_cap": round_price(float(it.get("lt") or 0.0)),
            "total_market_cap": round_price(float(it.get("zsz") or 0.0)),
            "turnover_rate": round_price(float(it.get("hs") or 0.0)),
            "consecutive_boards": int(it.get("lbc") or 0),
            "first_board_time": format_hms(str(it.get("fbt") or "")),
            "last_board_time": format_hms(str(it.get("lbt") or "")),
            "seal_funds": round_price(float(it.get("zj") or 0.0)),
            "broken_boards": int(it.get("zbc") or 0),
            "stat": str(it.get("tj") or ""),
        })
    return items
