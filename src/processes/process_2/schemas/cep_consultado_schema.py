from pydantic import BaseModel, ConfigDict, Field


class CepConsultadoSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cep: str = Field(alias="CEP")
    logradouro: str | None = Field(default=None, alias="Logradouro")
    complemento: str | None = Field(default=None, alias="Complemento")
    unidade: str | None = Field(default=None, alias="Unidade")
    bairro: str | None = Field(default=None, alias="Bairro")
    localidade: str | None = Field(default=None, alias="Localidade")
    uf: str | None = Field(default=None, alias="UF")
    estado: str | None = Field(default=None, alias="Estado")
    regiao: str | None = Field(default=None, alias="Região")
    ibge: str | None = Field(default=None, alias="IBGE")
    gia: str | None = Field(default=None, alias="GIA")
    ddd: str | None = Field(default=None, alias="DDD")
    siafi: str | None = Field(default=None, alias="SIAFI")
    status: str | None = Field(default=None, alias="Status")
