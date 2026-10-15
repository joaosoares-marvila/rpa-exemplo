from pydantic import BaseModel, field_validator


class CredenciaisSchema(BaseModel):
    login: str
    senha: str

    @field_validator("login", "senha")
    def validar_credenciais(cls, valor):
        if not valor:
            raise ValueError("O campo não pode estar vazio.")
        return valor