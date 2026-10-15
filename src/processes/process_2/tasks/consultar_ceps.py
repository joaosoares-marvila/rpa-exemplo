import os

from loguru import logger

from src.common.utils.excecoes import RegraNegocioError
from src.processes.process_2.apps import ViaCepApi
from src.processes.process_2.configs import ParametrosEstaticosProcesso
from src.processes.process_2.files import CepsConsultadosExcel, CepsGeradosExcel
from src.processes.process_2.schemas import CepConsultadoSchema


def consultar_ceps(viacep_api: ViaCepApi, caminho_arquivo_ceps_gerados: str) -> str:
    """ Consulta na ViaCEP os CEPs da planilha de CEPs gerados e persiste o resultado na planilha de CEPs consultados.

    Args:
        viacep_api (ViaCepApi): Cliente da API ViaCEP.
        caminho_arquivo_ceps_gerados (str): Caminho da planilha de CEPs gerados.

    Raises:
        Exception: Se ocorrer algum erro inesperado, uma exceção será lançada com a mensagem de erro.

    Returns:
        str: Caminho da planilha de CEPs consultados.
    """
    try:
        logger.info("Iniciando consulta de CEPs")

        ceps_gerados = CepsGeradosExcel(caminho_arquivo=caminho_arquivo_ceps_gerados).ler()
        ceps_consultados_excel = CepsConsultadosExcel(
            caminho_arquivo=os.path.join(ParametrosEstaticosProcesso.diretorio_temp, "ceps_consultados.xlsx")
        )
        ceps_consultados = []

        for cep in ceps_gerados:
            try:
                ceps_consultados.append(viacep_api.consultar_cep(cep=cep.cep))

            except RegraNegocioError as error:
                ceps_consultados.append(CepConsultadoSchema(cep=cep.cep, status=str(error)))
                logger.warning(f"CEP não consultado | {cep.cep} | {error}")

            except Exception as error:
                ceps_consultados.append(CepConsultadoSchema(cep=cep.cep, status=f"Erro inesperado | {error}"))
                logger.error(f"Erro inesperado ao consultar CEP | {cep.cep} | {error}")

        ceps_consultados_excel.salvar(ceps=ceps_consultados)

        logger.info("Consulta de CEPs finalizada")
        return ceps_consultados_excel.caminho_arquivo

    except Exception as error:
        raise Exception(f"Erro inesperado ao consultar CEPs | {error}")
