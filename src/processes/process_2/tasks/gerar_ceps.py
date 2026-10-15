import os

from loguru import logger

from src.processes.process_2.apps import InvertextoWeb
from src.processes.process_2.configs import ParametrosEstaticosProcesso
from src.processes.process_2.files import CepsGeradosExcel


def gerar_ceps(invertexto_web: InvertextoWeb, quantidade: int) -> str:
    """ Gera os CEPs no Invertexto e persiste o resultado na planilha de CEPs gerados.

    Args:
        invertexto_web (InvertextoWeb): Automação do gerador de CEP do Invertexto.
        quantidade (int): Quantidade de CEPs a serem gerados.

    Raises:
        Exception: Se ocorrer algum erro inesperado, uma exceção será lançada com a mensagem de erro.

    Returns:
        str: Caminho da planilha de CEPs gerados.
    """
    try:
        logger.info(f"Iniciando geração de CEPs | Quantidade: {quantidade}")

        ceps_gerados_excel = CepsGeradosExcel(
            caminho_arquivo=os.path.join(ParametrosEstaticosProcesso.diretorio_temp, "ceps_gerados.xlsx")
        )
        ceps_gerados = []

        for indice in range(1, quantidade + 1):
            try:
                logger.info(f"Gerando CEP {indice} de {quantidade}")
                ceps_gerados.append(invertexto_web.gerar_cep())

            except Exception as error:
                logger.error(f"Erro inesperado ao gerar CEP {indice} de {quantidade} | {error}")

        ceps_gerados_excel.salvar(ceps=ceps_gerados)

        logger.info(f"Geração de CEPs finalizada | {len(ceps_gerados)} de {quantidade} CEPs gerados")
        return ceps_gerados_excel.caminho_arquivo

    except Exception as error:
        raise Exception(f"Erro inesperado ao gerar CEPs | {error}")
