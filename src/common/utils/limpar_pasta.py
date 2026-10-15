import os
import time

from loguru import logger


def limpar_pasta(caminho_pasta: str, dias_retencao: int = None, recursivo: bool = False) -> None:
    """ Remove os arquivos de uma pasta, opcionalmente respeitando um período de retenção.

    Args:
        caminho_pasta (str): Caminho da pasta que deverá ser limpa.
        dias_retencao (int, optional): Quando informado, remove apenas os arquivos cuja última modificação
            seja anterior à quantidade de dias informada. Defaults to None (remove todos os arquivos).
        recursivo (bool, optional): Indica se as pastas filhas também devem ser percorridas. Defaults to False.

    Raises:
        FileNotFoundError: Se a pasta informada não existir.
        NotADirectoryError: Se o caminho informado não for uma pasta.
        ValueError: Se a quantidade de dias de retenção for negativa.
        Exception: Se ocorrer algum erro inesperado ao limpar a pasta.

    """
    try:
        if not os.path.exists(caminho_pasta):
            raise FileNotFoundError(f"A pasta '{caminho_pasta}' não foi encontrada.")

        if not os.path.isdir(caminho_pasta):
            raise NotADirectoryError(f"O caminho '{caminho_pasta}' não é uma pasta.")

        if dias_retencao is not None and dias_retencao < 0:
            raise ValueError("Os dias de retenção não podem ser negativos.")

        limite = None
        if dias_retencao is not None:
            limite = time.time() - dias_retencao * 24 * 60 * 60

        removidos = 0

        for raiz, pastas, arquivos in os.walk(caminho_pasta):
            for nome in arquivos:
                caminho_arquivo = os.path.join(raiz, nome)

                if limite is not None and os.path.getmtime(caminho_arquivo) >= limite:
                    continue

                os.remove(caminho_arquivo)
                removidos += 1

            if not recursivo:
                break

        logger.info(f"Limpeza da pasta '{caminho_pasta}' concluída. {removidos} arquivos removidos.")


    except (FileNotFoundError, NotADirectoryError, ValueError):
        raise

    except Exception as error:
        raise Exception(f"Erro inesperado ao limpar a pasta '{caminho_pasta}' | {error}")
