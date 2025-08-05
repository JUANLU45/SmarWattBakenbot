# expert_bot_api_COPY/utils/timezone_utils.py
# 🏢 UTILIDAD EMPRESARIAL PARA ZONA HORARIA ESPAÑOLA
"""
Utilidad robusta para manejo de zona horaria española (Madrid)
Maneja automáticamente el cambio entre CET (invierno) y CEST (verano)
"""

from datetime import datetime, timezone, timedelta


def get_spanish_timezone() -> timezone:
    """
    Obtiene la zona horaria española correcta (CET/CEST)

    Returns:
        timezone: Zona horaria española con offset correcto
    """
    now_utc = datetime.now(timezone.utc)

    # Determinar si estamos en horario de verano (CEST) o invierno (CET)
    # Horario de verano: último domingo de marzo al último domingo de octubre
    year = now_utc.year

    # Calcular último domingo de marzo
    march_last_sunday = _get_last_sunday_of_month(year, 3)

    # Calcular último domingo de octubre
    october_last_sunday = _get_last_sunday_of_month(year, 10)

    # Verificar si estamos en horario de verano (CEST: UTC+2) o invierno (CET: UTC+1)
    if march_last_sunday <= now_utc.replace(tzinfo=None) < october_last_sunday:
        # Horario de verano (CEST): UTC+2
        return timezone(timedelta(hours=2))
    else:
        # Horario de invierno (CET): UTC+1
        return timezone(timedelta(hours=1))


def _get_last_sunday_of_month(year: int, month: int) -> datetime:
    """
    Calcula el último domingo de un mes específico

    Args:
        year: Año
        month: Mes (1-12)

    Returns:
        datetime: Fecha del último domingo del mes
    """
    # Último día del mes
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)

    # Encontrar el último domingo
    days_back = (last_day.weekday() + 1) % 7
    last_sunday = last_day - timedelta(days=days_back)

    return last_sunday


def now_spanish() -> datetime:
    """
    Obtiene la fecha y hora actual en zona horaria española

    Returns:
        datetime: Fecha y hora actual en España
    """
    return datetime.now(get_spanish_timezone())


def now_spanish_iso() -> str:
    """
    Obtiene la fecha y hora actual en zona horaria española en formato ISO

    Returns:
        str: Fecha y hora actual en España en formato ISO
    """
    return now_spanish().isoformat()


def utc_to_spanish(utc_dt: datetime) -> datetime:
    """
    Convierte una fecha UTC a zona horaria española

    Args:
        utc_dt: Datetime en UTC

    Returns:
        datetime: Datetime en zona horaria española
    """
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    elif utc_dt.tzinfo != timezone.utc:
        utc_dt = utc_dt.astimezone(timezone.utc)

    return utc_dt.astimezone(get_spanish_timezone())


def spanish_to_utc(spanish_dt: datetime) -> datetime:
    """
    Convierte una fecha en zona horaria española a UTC

    Args:
        spanish_dt: Datetime en zona horaria española

    Returns:
        datetime: Datetime en UTC
    """
    if spanish_dt.tzinfo is None:
        spanish_dt = spanish_dt.replace(tzinfo=get_spanish_timezone())

    return spanish_dt.astimezone(timezone.utc)
