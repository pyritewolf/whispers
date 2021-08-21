from fastapi import HTTPException, status


# Custom 404 to return from api
class NotFoundException(HTTPException):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 400


CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tenés los permisos necesarios para esta acción",
)


def get_pydanticlike_error(entity: str, message: str):
    return [{"loc": ["body", entity, "__root__"], "msg": message}]


def get_pydanticlike_exception(
    entity: str, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
):
    return HTTPException(
        status_code=status_code,
        detail=get_pydanticlike_error(
            "auth",
            "Hubo un problema enviando el correo de cambio de contraseña. \
            Por favor, intente nuevamente.",
        ),
    )
