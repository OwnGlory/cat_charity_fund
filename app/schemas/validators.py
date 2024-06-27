from pydantic import BaseModel


class ValidationError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Пример сообщения об ошибке"
            }
        }