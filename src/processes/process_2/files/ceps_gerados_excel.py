from pathlib import Path

import pandas as pd
from loguru import logger

from src.processes.process_2.schemas import CepGeradoSchema


class CepsGeradosExcel:
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

    def ler(self) -> list[CepGeradoSchema]:
        """ Lê a planilha de CEPs gerados e converte cada linha em um CepGeradoSchema.

        Raises:
            Exception: Se ocorrer algum erro durante a leitura ou validação, uma exceção será lançada com a mensagem de erro.

        Returns:
            list[CepGeradoSchema]: CEPs contidos na planilha.
        """
        try:
            logger.info(f"Lendo planilha de CEPs gerados | {self.__caminho_arquivo}")

            tabela = pd.read_excel(io=self.__caminho_arquivo, dtype=str, keep_default_na=False)
            ceps = [CepGeradoSchema(**linha) for linha in tabela.to_dict("records")]

            logger.info(f"Planilha de CEPs gerados lida com sucesso | {len(ceps)} CEPs")
            return ceps

        except Exception as error:
            raise Exception(f"Erro inesperado ao ler planilha de CEPs gerados | {error}")

    def salvar(self, ceps: list[CepGeradoSchema]) -> None:
        """ Salva os CEPs gerados em uma planilha, criando a pasta caso ela não exista.

        Args:
            ceps (list[CepGeradoSchema]): CEPs gerados que serão salvos.

        Raises:
            Exception: Se ocorrer algum erro ao salvar a planilha, uma exceção será lançada com a mensagem de erro.
        """
        try:
            logger.info(f"Salvando planilha de CEPs gerados | {self.__caminho_arquivo}")

            self.__caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

            colunas = [campo.alias for campo in CepGeradoSchema.model_fields.values()]
            tabela = pd.DataFrame([cep.model_dump(by_alias=True) for cep in ceps], columns=colunas)
            tabela.to_excel(excel_writer=self.__caminho_arquivo, index=False)

            logger.info(f"Planilha de CEPs gerados salva com sucesso | {len(ceps)} CEPs")

        except Exception as error:
            raise Exception(f"Erro inesperado ao salvar planilha de CEPs gerados | {error}")
