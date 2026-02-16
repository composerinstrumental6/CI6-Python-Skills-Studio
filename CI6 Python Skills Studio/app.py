import os

from flask import Flask, render_template, request, session

from toolkit import (
    cipher_transform,
    convert_fuel_consumption,
    convert_currency,
    convert_scientific_prefix,
    count_date_distance,
    get_fx_rate_with_fallback,
    summarize_text,
)


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")


def base_context() -> dict:
    return {
        "text": "",
        "summary": None,
        "cipher_text": "",
        "cipher_type": "caesar",
        "cipher_mode": "encode",
        "cipher_key": "",
        "cipher_output": "",
        "cipher_error": None,
        "currency_amount": "",
        "currency_from": "USD",
        "currency_to": "EUR",
        "currency_result": None,
        "currency_rate": None,
        "currency_source": "",
        "currency_last_updated": "",
        "currency_error": None,
        "fuel_value": "",
        "fuel_from_unit": "mpg_us",
        "fuel_to_unit": "km_per_l",
        "fuel_output": None,
        "fuel_error": None,
        "reference_date": "",
        "target_date": "",
        "date_result": None,
        "date_error": None,
        "sci_value": "",
        "sci_from_prefix": "base",
        "sci_to_prefix": "mega",
        "sci_converted": None,
        "sci_notation": "",
        "sci_error": None,
    }


TOOL_FIELDS = {
    "analyze": ["text", "summary"],
    "cipher": ["cipher_text", "cipher_type", "cipher_mode", "cipher_key", "cipher_output", "cipher_error"],
    "currency": [
        "currency_amount",
        "currency_from",
        "currency_to",
        "currency_result",
        "currency_rate",
        "currency_source",
        "currency_last_updated",
        "currency_error",
    ],
    "fuel": ["fuel_value", "fuel_from_unit", "fuel_to_unit", "fuel_output", "fuel_error"],
    "date-counter": ["reference_date", "target_date", "date_result", "date_error"],
    "scientific": [
        "sci_value",
        "sci_from_prefix",
        "sci_to_prefix",
        "sci_converted",
        "sci_notation",
        "sci_error",
    ],
}


def get_context() -> dict:
    context = session.get("context")
    if not context:
        context = base_context()
    defaults = base_context()
    defaults.update(context)
    return defaults


def save_context(context: dict) -> None:
    session["context"] = context


@app.get("/")
def home():
    context = get_context()
    save_context(context)
    return render_template("index.html", **context)


@app.post("/analyze")
def analyze():
    text = request.form.get("text", "")
    summary = summarize_text(text)
    context = get_context()
    context.update({"text": text, "summary": summary})
    save_context(context)
    return render_template("index.html", **context)


@app.post("/cipher")
def cipher():
    cipher_text = request.form.get("cipher_text", "")
    cipher_type = request.form.get("cipher_type", "caesar")
    cipher_mode = request.form.get("cipher_mode", "encode")
    cipher_key = request.form.get("cipher_key", "")

    try:
        output = cipher_transform(cipher_type, cipher_mode, cipher_text, cipher_key)
        error = None
    except ValueError as exc:
        output = ""
        error = str(exc)

    context = get_context()
    context.update(
        {
            "cipher_text": cipher_text,
            "cipher_type": cipher_type,
            "cipher_mode": cipher_mode,
            "cipher_key": cipher_key,
            "cipher_output": output,
            "cipher_error": error,
        }
    )
    save_context(context)
    return render_template("index.html", **context)


@app.post("/currency")
def currency():
    amount_raw = request.form.get("currency_amount", "")
    currency_from = request.form.get("currency_from", "USD")
    currency_to = request.form.get("currency_to", "EUR")
    try:
        rate, source, last_updated = get_fx_rate_with_fallback(currency_from, currency_to)
        converted = convert_currency(float(amount_raw), rate)
        currency_error = None
    except ValueError as exc:
        converted, rate, source, last_updated = None, None, "", ""
        currency_error = str(exc)

    context = get_context()
    context.update(
        {
            "currency_amount": amount_raw,
            "currency_from": currency_from,
            "currency_to": currency_to,
            "currency_result": converted,
            "currency_rate": rate,
            "currency_source": source,
            "currency_last_updated": last_updated,
            "currency_error": currency_error,
        }
    )
    save_context(context)
    return render_template("index.html", **context)


@app.post("/fuel")
def fuel():
    fuel_value_raw = request.form.get("fuel_value", "")
    fuel_from_unit = request.form.get("fuel_from_unit", "mpg_us")
    fuel_to_unit = request.form.get("fuel_to_unit", "km_per_l")
    try:
        fuel_output = convert_fuel_consumption(float(fuel_value_raw), fuel_from_unit, fuel_to_unit)
        fuel_error = None
    except ValueError as exc:
        fuel_output = None
        fuel_error = str(exc)

    context = get_context()
    context.update(
        {
            "fuel_value": fuel_value_raw,
            "fuel_from_unit": fuel_from_unit,
            "fuel_to_unit": fuel_to_unit,
            "fuel_output": fuel_output,
            "fuel_error": fuel_error,
        }
    )
    save_context(context)
    return render_template("index.html", **context)


@app.post("/date-counter")
def date_counter():
    reference_date = request.form.get("reference_date", "")
    target_date = request.form.get("target_date", "")
    try:
        date_result = count_date_distance(reference_date, target_date)
        date_error = None
    except ValueError as exc:
        date_result = None
        date_error = str(exc)

    context = get_context()
    context.update(
        {
            "reference_date": reference_date,
            "target_date": target_date,
            "date_result": date_result,
            "date_error": date_error,
        }
    )
    save_context(context)
    return render_template("index.html", **context)


@app.post("/scientific")
def scientific():
    sci_value_raw = request.form.get("sci_value", "")
    sci_from_prefix = request.form.get("sci_from_prefix", "base")
    sci_to_prefix = request.form.get("sci_to_prefix", "mega")
    try:
        sci_converted, sci_notation = convert_scientific_prefix(
            float(sci_value_raw), sci_from_prefix, sci_to_prefix
        )
        sci_error = None
    except ValueError as exc:
        sci_converted, sci_notation = None, ""
        sci_error = str(exc)

    context = get_context()
    context.update(
        {
            "sci_value": sci_value_raw,
            "sci_from_prefix": sci_from_prefix,
            "sci_to_prefix": sci_to_prefix,
            "sci_converted": sci_converted,
            "sci_notation": sci_notation,
            "sci_error": sci_error,
        }
    )
    save_context(context)
    return render_template("index.html", **context)


@app.post("/clear")
def clear_tool():
    tool = request.form.get("tool", "")
    context = get_context()
    defaults = base_context()
    for field in TOOL_FIELDS.get(tool, []):
        context[field] = defaults[field]
    save_context(context)
    return render_template("index.html", **context)


@app.post("/clear-all")
def clear_all():
    context = base_context()
    save_context(context)
    return render_template("index.html", **context)


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5050"))
    app.run(debug=True, host=host, port=port)
