from datetime import date, datetime
from pathlib import Path

import pandas as pd
from loguru import logger

from src.processes.process_1.schemas import DespesaSchema


class RelatorioDespesasExcel:
    def __init__(self, caminho_arquivo: Path | str):
        self.__caminho_arquivo = Path(caminho_arquivo)

    def ler(self) -> list[DespesaSchema]:
        """ Lê o relatório de despesas e converte cada linha em um DespesaSchema.

        Raises:
            Exception: Se ocorrer algum erro durante a leitura ou validação, uma exceção será lançada com a mensagem de erro.

        Returns:
            list[DespesaSchema]: Despesas contidas no arquivo.
        """
        try:
            logger.info(f"Lendo relatório de despesas | {self.__caminho_arquivo}")

            tabela = pd.read_excel(self.__caminho_arquivo, dtype=str, keep_default_na=False)
            despesas = [DespesaSchema(**linha) for linha in tabela.to_dict("records")]

            logger.info(f"Relatório de despesas lido com sucesso | {len(despesas)} despesas")
            return despesas

        except Exception as error:
            raise Exception(f"Erro inesperado ao ler relatório de despesas | {error}")

    def atualizar_status(self, despesa: DespesaSchema) -> None:
        """Atualiza toda a linha da planilha correspondente ao Id da despesa, com base na versão atual da despesa.

        Args:
            despesa (DespesaSchema): Despesa com as informações atualizadas.

        Raises:
            Exception: Se a despesa não for encontrada ou ocorrer algum erro ao salvar o arquivo.
        """
        try:
            logger.info(f"Atualizando despesa no relatório de despesas | Id: {despesa.id}")

            tabela = pd.read_excel(self.__caminho_arquivo, dtype=str, keep_default_na=False)

            if "Id" not in tabela.columns:
                raise ValueError("Coluna 'Id' não encontrada no relatório")

            linhas = tabela["Id"].str.strip() == despesa.id.strip()
            if not linhas.any():
                raise ValueError(f"Despesa com Id {despesa.id} não encontrada no relatório")

            for coluna, valor in despesa.model_dump(by_alias=True).items():
                if valor is None:
                    valor = ""
                elif isinstance(valor, datetime):
                    valor = valor.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(valor, date):
                    valor = valor.strftime("%Y-%m-%d 00:00:00")
                tabela.loc[linhas, coluna] = str(valor)

            tabela.to_excel(self.__caminho_arquivo, index=False)

            logger.info(f"Despesa atualizada com sucesso no relatório de despesas | Id: {despesa.id}")

        except Exception as error:
            raise Exception(f"Erro inesperado ao atualizar despesa no relatório de despesas | {error}")
