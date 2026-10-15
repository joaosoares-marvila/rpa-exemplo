from loguru import logger
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.processes.process_2.schemas import CepGeradoSchema


class InvertextoWeb:
    def __init__(self, driver: Chrome):
        """ Inicializa o Invertexto e acessa a página do gerador de CEP.

        Args:
            driver (Chrome): Driver do navegador utilizado na automação.

        Raises:
            Exception: Se ocorrer algum erro ao acessar a página, uma exceção será lançada com a mensagem de erro.
        """
        self.__driver = driver

        self.__dominio = "https://www.invertexto.com/gerador-de-cep"
        self.__acessar()

    def __acessar(self):
        """ Acessa a página do gerador de CEP do Invertexto.

        Raises:
            Exception: Se ocorrer algum erro ao acessar a página, uma exceção será lançada com a mensagem de erro.
        """
        try:
            logger.info("Acessando gerador de CEP do Invertexto")

            self.__driver.get(url=self.__dominio)

            WebDriverWait(driver=self.__driver, timeout=10).until(
                method=EC.element_to_be_clickable(mark=(By.ID, "gerar"))
            )

            logger.info("Gerador de CEP do Invertexto acessado com sucesso")

        except Exception as error:
            raise Exception(f"Erro inesperado ao acessar o gerador de CEP do Invertexto | {error}")

    def __obter_valor_campo(self, id_campo: str) -> str:
        """ Obtém o valor de um campo da página do gerador de CEP.

        Args:
            id_campo (str): ID do elemento HTML do campo.

        Returns:
            str: Valor do campo, ou string vazia caso ele não possua valor.
        """
        return self.__driver.find_element(by=By.ID, value=id_campo).get_attribute("value") or ""

    def gerar_cep(self) -> CepGeradoSchema:
        """ Gera um novo CEP no Invertexto.

        Raises:
            Exception: Se ocorrer algum erro durante a geração do CEP, uma exceção será lançada com a mensagem de erro.

        Returns:
            CepGeradoSchema: Dados do CEP gerado.
        """
        try:
            logger.info("Gerando CEP no Invertexto")

            cep_anterior = self.__obter_valor_campo(id_campo="cep")

            WebDriverWait(driver=self.__driver, timeout=10).until(
                method=EC.element_to_be_clickable(mark=(By.ID, "gerar"))
            ).click()

            WebDriverWait(driver=self.__driver, timeout=10).until(
                method=lambda _: self.__obter_valor_campo(id_campo="cep") not in ("", cep_anterior)
            )

            cep_gerado = CepGeradoSchema(
                cep=self.__obter_valor_campo(id_campo="cep"),
                endereco=self.__obter_valor_campo(id_campo="endereco"),
                bairro=self.__obter_valor_campo(id_campo="bairro"),
                cidade=self.__obter_valor_campo(id_campo="cidade"),
                uf=self.__obter_valor_campo(id_campo="uf"),
            )

            logger.success(f"CEP gerado com sucesso | {cep_gerado}")
            return cep_gerado

        except Exception as error:
            raise Exception(f"Erro inesperado ao gerar CEP no Invertexto | {error}")
