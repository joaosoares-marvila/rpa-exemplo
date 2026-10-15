import re

import requests
from loguru import logger

from src.common.utils.excecoes import RegraNegocioError
from src.processes.process_2.schemas import CepConsultadoSchema


class ViaCepApi:
    def __init__(self):
        """ Inicializa o cliente da API ViaCEP. """
        self.__dominio = "https://viacep.com.br/ws"

    def consultar_cep(self, cep: str) -> CepConsultadoSchema:
        """ Consulta um CEP na API ViaCEP.

        Args:
            cep (str): CEP a ser consultado, com ou sem pontuação.

        Raises:
            RegraNegocioError: Se o CEP for inválido ou não for encontrado na ViaCEP.
            Exception: Se ocorrer algum erro inesperado durante a consulta, uma exceção será lançada com a mensagem de erro.

        Returns:
            CepConsultadoSchema: Dados do CEP retornados pela ViaCEP.
        """
        try:
            logger.info(f"Consultando CEP na ViaCEP | {cep}")

            cep_numerico = re.sub(pattern=r"\D", repl="", string=cep)
            if len(cep_numerico) != 8:
                raise RegraNegocioError(f"CEP inválido | {cep}")

            resposta = requests.get(url=f"{self.__dominio}/{cep_numerico}/json/", timeout=30)
            resposta.raise_for_status()
            dados = resposta.json()

            if dados.get("erro"):
                raise RegraNegocioError("CEP não encontrado na ViaCEP")

            cep_consultado = CepConsultadoSchema(**dados, status="OK")

            logger.success(f"CEP consultado com sucesso | {cep_consultado}")
            return cep_consultado

        except RegraNegocioError:
            raise

        except Exception as error:
            raise Exception(f"Erro inesperado ao consultar CEP na ViaCEP | {cep} | {error}")
