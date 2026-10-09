"""Строгий ограниченный валидатор используемой части встроенной схемы."""
import json
import re
from datetime import datetime, timezone
from importlib.resources import files

MAX_BYTES = 1_048_576


class InputError(ValueError):
    """Безопасная ошибка: только пути схемы, без значений ввода."""


def timestamp(value):
    try:
        if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])", value) is None:
            raise ValueError
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None or result.utcoffset() is None:
            raise ValueError
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        raise InputError("неверное время с часовым поясом") from None


def validate(value, schema, path="input"):
    types = {"object": dict, "string": str, "integer": int, "boolean": bool}
    if type(value) is not types[schema["type"]]:
        raise InputError(f"{path}: неверный тип")
    if "const" in schema and value != schema["const"]:
        raise InputError(f"{path}: неподдерживаемая версия")
    if "enum" in schema and value not in schema["enum"]:
        raise InputError(f"{path}: неверный вариант")
    if isinstance(value, dict):
        if set(value) - set(schema["properties"]):
            raise InputError(f"{path}: неизвестное поле")
        if set(schema["required"]) - set(value):
            raise InputError(f"{path}: нет обязательного поля")
        for key, child in value.items():
            validate(child, schema["properties"][key], f"{path}.{key}")
    elif type(value) is int:
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            raise InputError(f"{path}: вне диапазона")
    elif isinstance(value, str):
        if len(value) > schema.get("maxLength", len(value)):
            raise InputError(f"{path}: слишком длинная строка")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            raise InputError(f"{path}: неверный псевдоним")
        if schema.get("format") == "date-time":
            timestamp(value)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("повторный ключ JSON")
        result[key] = value
    return result


def _constant(_value):
    raise InputError("бесконечное число или NaN в JSON")


def load(raw):
    if len(raw) > MAX_BYTES:
        raise InputError("вход превышает 1 МиБ")
    try:
        value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, UnicodeDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, InputError):
            raise
        raise InputError("неверный JSON") from None
    schema = json.loads(files("vps_opsec_auditor").joinpath("input-v1.schema.json").read_text())
    validate(value, schema)
    for item in value["checks"].values():
        if value["synthetic"] != (item["source"] == "synthetic"):
            raise InputError("признак synthetic не соответствует источнику")
        if item["state"] != "observed" and item["facts"]:
            raise InputError("состояние не observed требует пустых facts")
    return value
