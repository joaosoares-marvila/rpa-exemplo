from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


class DespesaSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="Id")
    data: date | None = Field(default=None, alias="Date")
    solicitante: str = Field(alias="Requester")
    categoria: str = Field(alias="Category")
    valor: Decimal = Field(alias="Value")
    descricao: str | None = Field(default=None, alias="Description")
    status: str | None = Field(default=None, alias="Status")

    @field_validator("data", mode="before")
    def converter_data(cls, valor: Any):
        if isinstance(valor, str):
            valor = valor.strip()
            if not valor:
                return None
            formato = "%Y-%m-%d %H:%M:%S" if "-" in valor else "%d/%m/%Y"
            return datetime.strptime(valor, formato).date()
        return valor

    @field_validator("descricao", "status", mode="before")
    def opcional_vazio_para_none(cls, valor: Any):
        if isinstance(valor, str) and not valor.strip():
            return None
        return valor

    @field_validator("id", "solicitante", "categoria")
    def validar_obrigatorio(cls, valor: str):
        if not valor.strip():
            raise ValueError("O campo não pode estar vazio.")
        return valor
