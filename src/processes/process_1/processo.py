from contextlib import suppress

from loguru import logger

from src.common.configs import ParametrosExecucaoCompartilhado
from src.common.utils import enviar_email, limpar_pasta, mover_arquivo, obter_driver
from src.processes.process_1.apps import IprocessWeb
from src.processes.process_1.configs import ParametrosEstaticosProcesso, ParametrosExecucaoProcesso
from src.processes.process_1.files import RelatorioDespesasExcel
from src.processes.process_1.tasks import registrar_despesas


def executar_processo_1() -> None:
    """ Executa o processo 1: baixa o relatório de despesas do iProcess Web, registra cada despesa, move o relatório para a pasta de saída e o envia por e-mail.

    Raises:
        Exception: Se ocorrer algum erro crítico durante a execução, uma exceção será lançada com a mensagem de erro.
    """
    driver = None
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
            login=ParametrosExecucaoProcesso.credenciais_iprocess_web.login,
            senha=ParametrosExecucaoProcesso.credenciais_iprocess_web.senha,
        )
        caminho_arquivo_relatorio_despesas = iprocess_web.baixar_relatorio_despesas()

        relatorio_despesas_excel = RelatorioDespesasExcel(caminho_arquivo=caminho_arquivo_relatorio_despesas)
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

        enviar_email(
            servidor=ParametrosExecucaoCompartilhado.smtp_servidor,
            porta=ParametrosExecucaoCompartilhado.smtp_porta,
            remetente=ParametrosExecucaoCompartilhado.credenciais_smtp.login,
            senha=ParametrosExecucaoCompartilhado.credenciais_smtp.senha,
            destinatarios=ParametrosEstaticosProcesso.destinatarios_email,
            assunto="Processo 1 - Relatório de despesas",
            corpo="Processo 1 finalizado com sucesso. O relatório de despesas segue em anexo.",
            anexos=[caminho_arquivo_relatorio_despesas],
            habilitado=ParametrosExecucaoCompartilhado.enviar_email,
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