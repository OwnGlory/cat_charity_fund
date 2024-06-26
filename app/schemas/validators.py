from pydantic import BaseModel


class ValidationError(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Validation error message"
            }
        }