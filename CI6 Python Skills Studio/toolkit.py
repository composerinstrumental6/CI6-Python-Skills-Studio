import json
from datetime import date, datetime
from time import time
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def summarize_text(text: str) -> dict:
    words = [w for w in text.split() if w.strip()]
    sentences = [s for s in text.replace("?", ".").replace("!", ".").split(".") if s.strip()]
    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
    }


def caesar_cipher(text: str, shift: int) -> str:
    def rotate(char: str, base: str) -> str:
        start = ord(base)
        return chr(start + ((ord(char) - start + shift) % 26))

    output = []
    for ch in text:
        if "a" <= ch <= "z":
            output.append(rotate(ch, "a"))
        elif "A" <= ch <= "Z":
            output.append(rotate(ch, "A"))
        else:
            output.append(ch)
    return "".join(output)


def atbash_cipher(text: str) -> str:
    output = []
    for ch in text:
        if "a" <= ch <= "z":
            output.append(chr(ord("z") - (ord(ch) - ord("a"))))
        elif "A" <= ch <= "Z":
            output.append(chr(ord("Z") - (ord(ch) - ord("A"))))
        else:
            output.append(ch)
    return "".join(output)


def vigenere_cipher(text: str, key: str, decode: bool = False) -> str:
    letters = [c.lower() for c in key if c.isalpha()]
    if not letters:
        raise ValueError("Vigenere requires an alphabetic key.")

    output = []
    key_index = 0
    for ch in text:
        if ch.isalpha():
            k = ord(letters[key_index % len(letters)]) - ord("a")
            shift = -k if decode else k
            base = "A" if ch.isupper() else "a"
            output.append(chr(ord(base) + ((ord(ch) - ord(base) + shift) % 26)))
            key_index += 1
        else:
            output.append(ch)
    return "".join(output)


MORSE_MAP = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}
MORSE_REVERSE_MAP = {v: k for k, v in MORSE_MAP.items()}


def morse_encode(text: str) -> str:
    words = []
    for word in text.upper().split(" "):
        chars = []
        for ch in word:
            if ch in MORSE_MAP:
                chars.append(MORSE_MAP[ch])
            else:
                chars.append(ch)
        words.append(" ".join(chars))
    return " / ".join(words)


def morse_decode(text: str) -> str:
    words = []
    for word in text.split("/"):
        chars = []
        for token in word.strip().split():
            chars.append(MORSE_REVERSE_MAP.get(token, token))
        words.append("".join(chars))
    return " ".join(words)


def cipher_transform(cipher_type: str, mode: str, text: str, key: str = "") -> str:
    if cipher_type == "caesar":
        if key.strip() == "":
            raise ValueError("Caesar requires a numeric shift key.")
        try:
            shift = int(key)
        except ValueError:
            raise ValueError("Caesar key must be an integer.")
        if mode == "decode":
            shift = -shift
        return caesar_cipher(text, shift)

    if cipher_type == "morse":
        return morse_decode(text) if mode == "decode" else morse_encode(text)

    if cipher_type == "atbash":
        return atbash_cipher(text)

    if cipher_type == "rot13":
        return caesar_cipher(text, 13)

    if cipher_type == "vigenere":
        return vigenere_cipher(text, key, decode=(mode == "decode"))

    raise ValueError("Unsupported cipher type.")


def tip_split(amount: float, percent: float, people: int) -> tuple[float, float]:
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if percent < 0:
        raise ValueError("Tip percent cannot be negative.")
    if people <= 0:
        raise ValueError("People must be at least 1.")

    total = amount * (1 + (percent / 100))
    per_person = total / people
    return round(total, 2), round(per_person, 2)


def fetch_yahoo_fx_rate(from_currency: str, to_currency: str) -> float:
    from_code = from_currency.upper().strip()
    to_code = to_currency.upper().strip()
    if len(from_code) != 3 or len(to_code) != 3:
        raise ValueError("Currency codes must be 3 letters (example: USD, EUR).")

    symbol = f"{from_code}{to_code}=X"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol)}"
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            },
        )
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise ValueError(f"Could not reach Yahoo Finance: {exc.reason}")
    except Exception:
        raise ValueError("Could not read Yahoo Finance response.")

    try:
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        price = meta.get("regularMarketPrice") or meta.get("previousClose")
    except (KeyError, IndexError, TypeError):
        raise ValueError("Unexpected Yahoo Finance data format.")

    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Yahoo Finance returned an invalid exchange rate.")
    return float(price)


def convert_currency(amount: float, rate: float) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if rate <= 0:
        raise ValueError("Exchange rate must be greater than 0.")
    return round(amount * rate, 4)


FX_CACHE: dict[str, tuple[float, float]] = {}
FX_CACHE_TTL_SECONDS = 600
SNAPSHOT_DATE = "2026-02-16"
SNAPSHOT_USD_BASED = {
    "USD": 1.0,
    "EUR": 0.95,
    "JPY": 150.2,
    "GBP": 0.79,
    "CNY": 7.22,
    "AUD": 1.54,
    "CAD": 1.35,
    "CHF": 0.88,
    "HKD": 7.82,
    "SGD": 1.34,
}


def _snapshot_fx_rate(from_currency: str, to_currency: str) -> float:
    from_code = from_currency.upper().strip()
    to_code = to_currency.upper().strip()
    if from_code not in SNAPSHOT_USD_BASED or to_code not in SNAPSHOT_USD_BASED:
        raise ValueError("Snapshot does not include one of the selected currencies.")

    usd_to_from = SNAPSHOT_USD_BASED[from_code]
    usd_to_to = SNAPSHOT_USD_BASED[to_code]
    return usd_to_to / usd_to_from


def get_fx_rate_with_fallback(from_currency: str, to_currency: str) -> tuple[float, str, str]:
    key = f"{from_currency.upper()}:{to_currency.upper()}"
    now = time()
    cached = FX_CACHE.get(key)
    if cached and (now - cached[1]) < FX_CACHE_TTL_SECONDS:
        return cached[0], "Yahoo Finance (cached)", datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        rate = fetch_yahoo_fx_rate(from_currency, to_currency)
        FX_CACHE[key] = (rate, now)
        return rate, "Yahoo Finance (live)", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        message = str(exc)
        if "Too Many Requests" in message or "429" in message or "Could not reach Yahoo Finance" in message:
            rate = _snapshot_fx_rate(from_currency, to_currency)
            return rate, "Snapshot fallback", SNAPSHOT_DATE
        raise


def convert_fuel_consumption(value: float, from_unit: str, to_unit: str) -> float:
    if value <= 0:
        raise ValueError("Fuel value must be greater than 0.")

    factors = {"mpg_us", "km_per_l", "l_per_100km"}
    if from_unit not in factors or to_unit not in factors:
        raise ValueError("Invalid fuel unit selection.")

    if from_unit == "mpg_us":
        km_per_l = value * 0.425143707
    elif from_unit == "km_per_l":
        km_per_l = value
    else:
        km_per_l = 100 / value

    if to_unit == "km_per_l":
        return round(km_per_l, 6)
    if to_unit == "mpg_us":
        return round(km_per_l / 0.425143707, 6)
    return round(100 / km_per_l, 6)


def _add_months_safe(start: date, months: int) -> date:
    year = start.year + (start.month - 1 + months) // 12
    month = (start.month - 1 + months) % 12 + 1
    day = start.day
    while True:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1


def count_date_distance(reference_date: str, target_date: str) -> dict:
    try:
        ref = datetime.strptime(reference_date, "%Y-%m-%d").date()
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Use YYYY-MM-DD for both dates.")

    delta_days = (target - ref).days
    direction = "future" if delta_days > 0 else "past" if delta_days < 0 else "today"

    start, end = (ref, target) if ref <= target else (target, ref)
    months = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:
        months -= 1
    month_anchor = _add_months_safe(start, months)
    leftover_days = (end - month_anchor).days
    weeks = round(abs(delta_days) / 7, 2)

    years = months // 12
    rem_months = months % 12
    year_label = "year" if years == 1 else "years"
    month_label = "month" if rem_months == 1 else "months"
    day_label = "day" if leftover_days == 1 else "days"
    parts = [f"{years} {year_label}", f"{rem_months} {month_label}", f"{leftover_days} {day_label}"]
    span = ", ".join(parts)
    if direction == "future":
        human_span = f"in {span}"
    elif direction == "past":
        human_span = f"{span} ago"
    else:
        human_span = "today"

    return {
        "target_weekday": target.strftime("%A"),
        "delta_days": delta_days,
        "direction": direction,
        "weeks": weeks,
        "years": years,
        "months": rem_months,
        "remaining_days": leftover_days,
        "human_span": human_span,
    }


def convert_scientific_prefix(value: float, from_prefix: str, to_prefix: str) -> tuple[float, str]:
    exponents = {
        "pico": -12,
        "nano": -9,
        "micro": -6,
        "milli": -3,
        "base": 0,
        "kilo": 3,
        "mega": 6,
        "giga": 9,
    }
    if from_prefix not in exponents or to_prefix not in exponents:
        raise ValueError("Invalid prefix selection.")

    base_value = value * (10 ** exponents[from_prefix])
    converted = base_value / (10 ** exponents[to_prefix])

    if base_value == 0:
        sci = "0 x 10^0"
    else:
        sci_exp = int(f"{base_value:e}".split("e")[1])
        sci_coeff = base_value / (10 ** sci_exp)
        sci = f"{sci_coeff:.6g} x 10^{sci_exp}"
    return converted, sci
