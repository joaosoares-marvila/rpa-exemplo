from contextlib import suppress

from loguru import logger

from src.common.configs import ParametrosExecucaoCompartilhado
from src.common.utils import limpar_pasta, mover_arquivo, obter_driver
from src.processes.process_1.apps import IprocessWeb
from src.processes.process_1.configs import ParametrosEstaticosProcesso
from src.processes.process_1.files import RelatorioDespesasExcel
from src.processes.process_1.tasks import registrar_despesas


def executar_processo_1():
    try:
        logger.info("Iniciando processo 1")

        limpar_pasta(
            caminho_pasta=ParametrosEstaticosProcesso.diretorio_saida,
            recursivo=True
        )
        driver = obter_driver(
            headless=ParametrosExecucaoCompartilhado.headless,
            diretorio_download=ParametrosEstaticosProcesso.diretorio_download,
        )

        iprocess_web = IprocessWeb(
            driver=driver,
            login=ParametrosExecucaoCompartilhado.credenciais_iprocess_web.login,
            senha=ParametrosExecucaoCompartilhado.credenciais_iprocess_web.senha,
        )
        caminho_arquivo_relatorio_despesas = iprocess_web.baixar_relatorio_despesas()
        
        relatorio_despesas_excel = RelatorioDespesasExcel(caminho_arquivo_relatorio_despesas)
        despesas = relatorio_despesas_excel.ler()
        registrar_despesas(
            iprocess_web=iprocess_web,
            despesas=despesas,
            relatorio_despesas_excel=relatorio_despesas_excel
        )
        caminho_arquivo_relatorio_despesas = mover_arquivo(
            caminho_original=caminho_arquivo_relatorio_despesas,
            pasta_destino=ParametrosEstaticosProcesso.diretorio_saida,
        )

        logger.info("Processo 1 finalizado com sucesso")

    except Exception as error:
        raise Exception(f"Erro crítico e inesperado ao executar o processo 1 | {error}")

    finally:
        limpar_pasta(
            caminho_pasta=ParametrosEstaticosProcesso.diretorio_download,
            recursivo=True
        )
        with suppress(Exception):
            driver.quit()