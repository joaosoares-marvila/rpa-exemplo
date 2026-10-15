import os

from loguru import logger


def configurar_log(diretorio_logs: str, nome_processo: str) -> int:
    """ Adiciona ao loguru um arquivo de log diário para o processo, mantendo o log do console.

    Args:
        diretorio_logs (str): Pasta onde os arquivos de log serão gravados. Será criada se não existir.
        nome_processo (str): Nome do processo, usado como prefixo do arquivo (ex.: `processo_1`).

    Returns:
        int: Identificador do handler criado, para ser removido com `logger.remove` ao final do processo.

    Raises:
        Exception: Se ocorrer algum erro inesperado ao configurar o log.
    """
    try:
        os.makedirs(name=diretorio_logs, exist_ok=True)
        return logger.add(
            sink=os.path.join(diretorio_logs, f"{nome_processo}_{{time:YYYY-MM-DD}}.log"),
            encoding="utf-8",
        )

    except Exception as error:
        raise Exception(f"Erro inesperado ao configurar o log em '{diretorio_logs}' | {error}")
