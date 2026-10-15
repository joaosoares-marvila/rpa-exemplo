
from pathlib import Path

from loguru import logger
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.common.utils import aguardar_arquivo_criado
from src.processes.process_1.configs import ParametrosEstaticosProcesso
from src.processes.process_1.schemas import DespesaSchema


class IprocessWeb:
    def __init__(self, driver: Chrome, login: str, senha: str):
        self.__driver = driver
        self.__login = login
        self.__senha = senha

        self.__dominio = "https://www.iprocess.com.br/treinamento/rpa/login.html"
        self.__autenticar()

    def __autenticar(self):
        """ Autentica o usuário no iProcess Web.

        Raises:
            Exception: Se ocorrer algum erro durante a autenticação, uma exceção será lançada com a mensagem de erro.
        """        
        try:
            logger.info("Autenticando no iProcess Web")

            self.__driver.get(self.__dominio)

            campo_login = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Login"))
            )
            campo_login.send_keys(self.__login)

            campo_senha = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Senha"))
            )
            campo_senha.send_keys(self.__senha)

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnLogin"))
            ).click()

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'home.html')]"))
            )

            logger.info("Autenticado no iProcess Web com sucesso")

        except Exception as error:
            raise Exception(f"Erro ao inesperado ao autenticar no iProcess | {error}")

    def baixar_relatorio_despesas(self) -> str:
        """ Baixa o relatório de despesas do iProcess Web.

        Raises:
            Exception: Se ocorrer algum erro durante o download do relatório, uma exceção será lançada com a mensagem de erro.

        Returns:
            str: Caminho do arquivo baixado.
        """        
        try:
            logger.info("Baixando relatório de despesas")

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Expenses Report')]"))
            ).click()

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download Expenses Report')]"))
            ).click()

            caminho_arquivo = Path(ParametrosEstaticosProcesso.diretorio_download, "expenses.xlsx")

            if not aguardar_arquivo_criado(str(caminho_arquivo), tempo_maximo=60):
                raise FileNotFoundError(f"O arquivo '{caminho_arquivo}' não foi baixado no tempo esperado.")

            logger.info("Relatório de despesas baixado com sucesso")
            return caminho_arquivo
        
        except Exception as error:
            raise Exception(f"Erro inesperado ao baixar relatório de despesas | {error}")

    def registrar_despesa(self, despesa: DespesaSchema) -> str:
        """ Registra uma despesa no iProcess Web.

        Args:
            despesa: Objeto representando a despesa a ser registrada.

        Raises:
            Exception: Se ocorrer algum erro durante o registro da despesa, uma exceção será lançada com a mensagem de erro.

        Returns:
            str: Status do registro da despesa.
        """
        try:
            logger.info(f"Registrando despesa | {despesa}")

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Register Expense')]"))
            ).click()

            campo_id = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Id"))
            )
            campo_id.send_keys(despesa.id)

            campo_data = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Date"))
            )
            campo_data.send_keys(str(despesa.data))

            campo_solicitante = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Requester"))
            )
            campo_solicitante.send_keys(despesa.solicitante)

            select_categoria = Select(WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Category"))
            ))
            select_categoria.select_by_visible_text(despesa.categoria)

            campo_valor = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Value"))
            )
            campo_valor.send_keys(str(despesa.valor))

            campo_descricao = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Description"))
            )
            campo_descricao.send_keys(despesa.descricao or "Nenhuma descrição fornecida")

            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnRegister"))
            ).click()

            resultado_registro = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='content']//div"))
                ).text

            if "Despesa cadastrada com sucesso!" in resultado_registro:
                status = "OK"
                logger.success(f"Despesa registrada com sucesso | {despesa}")
            
            else:
                status = f"Erro ao registrar despesa | {resultado_registro}"
                logger.error(f"Erro ao registrar despesa | {despesa} | {resultado_registro}")

            return status
        
        except Exception as error:
            raise Exception(f"Erro inesperado ao registrar despesa no IProcessWeb | {despesa} | {error}")
