from pydantic import BaseModel, ConfigDict, Field, field_validator


class CepGeradoSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cep: str = Field(alias="CEP")
    endereco: str | None = Field(default=None, alias="Endereço")
    bairro: str | None = Field(default=None, alias="Bairro")
    cidade: str | None = Field(default=None, alias="Cidade")
    uf: str | None = Field(default=None, alias="UF")

    @field_validator("cep")
    def validar_obrigatorio(cls, valor: str) -> str:
        """ Valida que o CEP não está vazio e remove espaços nas extremidades.

        Args:
            valor (str): CEP informado.

        Raises:
            ValueError: Se o CEP estiver vazio.

        Returns:
            str: CEP sem espaços nas extremidades.
        """
        if not valor.strip():
            raise ValueError("O campo não pode estar vazio.")
        return valor.strip()
