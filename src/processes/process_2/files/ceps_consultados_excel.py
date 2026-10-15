from pathlib import Path

import pandas as pd
from loguru import logger

from src.processes.process_2.schemas import CepConsultadoSchema


class CepsConsultadosExcel:
    def __init__(self, caminho_arquivo: Path | str):
        """ Inicializa o manipulador da planilha.

        Args:
            caminho_arquivo (Path | str): Caminho da planilha.
        """
        self.__caminho_arquivo = Path(caminho_arquivo)

    @property
    def caminho_arquivo(self) -> str:
        """ Obtém o caminho da planilha.

        Returns:
            str: Caminho da planilha.
        """
        return str(self.__caminho_arquivo)

    def salvar(self, ceps: list[CepConsultadoSchema]) -> None:
        """ Salva os CEPs consultados em uma planilha, criando a pasta caso ela não exista.

        Args:
            ceps (list[CepConsultadoSchema]): CEPs consultados que serão salvos.

        Raises:
            Exception: Se ocorrer algum erro ao salvar a planilha, uma exceção será lançada com a mensagem de erro.
        """
        try:
            logger.info(f"Salvando planilha de CEPs consultados | {self.__caminho_arquivo}")

            self.__caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

            colunas = [campo.alias for campo in CepConsultadoSchema.model_fields.values()]
            tabela = pd.DataFrame([cep.model_dump(by_alias=True) for cep in ceps], columns=colunas)
            tabela.to_excel(excel_writer=self.__caminho_arquivo, index=False)

            logger.info(f"Planilha de CEPs consultados salva com sucesso | {len(ceps)} CEPs")

        except Exception as error:
            raise Exception(f"Erro inesperado ao salvar planilha de CEPs consultados | {error}")
