from loguru import logger

from src.common.utils.excecoes import RegraNegocioError
from src.processes.process_1.apps import IprocessWeb
from src.processes.process_1.files import RelatorioDespesasExcel
from src.processes.process_1.schemas import DespesaSchema


def registrar_despesas(iprocess_web: IprocessWeb, despesas: list[DespesaSchema], relatorio_despesas_excel: RelatorioDespesasExcel):
    try:
        logger.info("Iniciando registro de despesas")

        for despesa in despesas:
            try:
                logger.info(f"Registrando despesa | {despesa}")
                despesa.status = iprocess_web.registrar_despesa(despesa)
                relatorio_despesas_excel.atualizar_status(despesa=despesa)

            except Exception as error:
                despesa.status = f"Erro inesperado | {str(error)}"
                relatorio_despesas_excel.atualizar_status(despesa=despesa)
                logger.error(f"Erro inesperado ao registrar despesa | {despesa} | {error}")

        logger.info("Registro de despesas finalizado")

    except Exception as error:
        raise Exception(f"Erro inesperado ao registrar despesas | {error}")