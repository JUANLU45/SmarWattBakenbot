# smarwatt_auth/exceptions.py
# 🏢 EXCEPCIONES EMPRESARIALES PARA AUTENTICACIÓN


class AppError(Exception):
    """Excepción base empresarial"""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(AppError):
    """Error de autenticación empresarial"""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)


class AuthorizationError(AppError):
    """Error de autorización empresarial"""

    def __init__(self, message: str, status_code: int = 403):
        super().__init__(message, status_code)


class RateLimitError(AppError):
    """Error de límite de velocidad empresarial"""

    def __init__(self, message: str, status_code: int = 429):
        super().__init__(message, status_code)
