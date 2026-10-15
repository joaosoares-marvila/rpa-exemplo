from contextlib import suppress

from loguru import logger

from src.common.configs import ParametrosExecucaoCompartilhado
from src.common.utils import enviar_email, limpar_pasta, mover_arquivo, obter_driver
from src.processes.process_2.apps import InvertextoWeb, ViaCepApi
from src.processes.process_2.configs import ParametrosEstaticosProcesso, ParametrosExecucaoProcesso
from src.processes.process_2.tasks import consultar_ceps, gerar_ceps


def executar_processo_2() -> None:
    """ Executa o processo 2: gera CEPs no Invertexto, consulta cada CEP na ViaCEP, move as planilhas para a pasta de saída e as envia por e-mail.

    Raises:
        Exception: Se ocorrer algum erro crítico durante a execução, uma exceção será lançada com a mensagem de erro.
    """
    driver = None
    try:
        logger.info("Iniciando processo 2")

        quantidade_ceps = ParametrosExecucaoProcesso.quantidade_ceps
        if quantidade_ceps <= 0:
            raise ValueError(f"A quantidade de CEPs deve ser maior que zero | {quantidade_ceps}")

        limpar_pasta(
            caminho_pasta=ParametrosEstaticosProcesso.diretorio_saida,
            recursivo=True
        )
        driver = obter_driver(headless=ParametrosExecucaoCompartilhado.headless)

        # Task 1: gerar CEPs no Invertexto
        invertexto_web = InvertextoWeb(driver=driver)
        caminho_arquivo_ceps_gerados = gerar_ceps(invertexto_web=invertexto_web, quantidade=quantidade_ceps)

        # Task 2: consultar CEPs na ViaCEP
        viacep_api = ViaCepApi()
        caminho_arquivo_ceps_consultados = consultar_ceps(
            viacep_api=viacep_api,
            caminho_arquivo_ceps_gerados=caminho_arquivo_ceps_gerados,
        )

        caminhos_planilhas = [
            mover_arquivo(
                caminho_original=caminho_planilha,
                pasta_destino=ParametrosEstaticosProcesso.diretorio_saida,
            )
            for caminho_planilha in (caminho_arquivo_ceps_gerados, caminho_arquivo_ceps_consultados)
        ]

        enviar_email(
            servidor=ParametrosExecucaoCompartilhado.smtp_servidor,
            porta=ParametrosExecucaoCompartilhado.smtp_porta,
            remetente=ParametrosExecucaoCompartilhado.credenciais_smtp.login,
            senha=ParametrosExecucaoCompartilhado.credenciais_smtp.senha,
            destinatarios=ParametrosEstaticosProcesso.destinatarios_email,
            assunto="Processo 2 - CEPs gerados e consultados",
            corpo="Processo 2 finalizado com sucesso. As planilhas de CEPs gerados e consultados seguem em anexo.",
            anexos=caminhos_planilhas,
            habilitado=ParametrosExecucaoCompartilhado.enviar_email,
        )

        logger.info("Processo 2 finalizado com sucesso")

    except Exception as error:
        raise Exception(f"Erro crítico e inesperado ao executar o processo 2 | {error}")

    finally:
        limpar_pasta(
            caminho_pasta=ParametrosEstaticosProcesso.diretorio_temp,
            recursivo=True
        )
        with suppress(Exception):
            driver.quit()
