import re


def normalize_symbol(symbol: str) -> str:
    s = symbol.strip().lower()
    m = re.match(r"^(\d{6})\.(sh|sz)$", s)
    if m:
        return f"{m.group(2)}{m.group(1)}"
    m = re.match(r"^(sh|sz)\d{6}$", s)
    if m:
        return s
    m = re.match(r"^(\d{6})$", s)
    if m:
        code = m.group(1)
        prefix = "sh" if code.startswith("6") or code.startswith("9") else "sz"
        return f"{prefix}{code}"
    raise ValueError("symbol格式不正确")


def symbol_to_instrument(symbol: str) -> str:
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


def round_price(v: float) -> float:
    return float(f"{v:.2f}")


def limit_rate(code: str, name: str) -> float:
    n = name.upper()
    if n.startswith("*ST") or n.startswith("ST"):
        return 0.05
    if code.startswith("300") or code.startswith("301") or code.startswith("688"):
        return 0.20
    return 0.10


def format_hms(s: str) -> str:
    s = (s or "").strip()
    if len(s) == 6 and s.isdigit():
        return f"{s[0:2]}:{s[2:4]}:{s[4:6]}"
    return s
