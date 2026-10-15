import os
import time


def aguardar_arquivo_criado(caminho_arquivo: str, tempo_maximo: float = 30, intervalo: float = 0.5) -> bool:
    """ Aguarda a criação de um arquivo dentro do tempo máximo informado.

    Args:
        caminho_arquivo (str): Caminho completo do arquivo esperado.
        tempo_maximo (float, optional): Tempo máximo de espera, em segundos. Defaults to 30.
        intervalo (float, optional): Intervalo entre cada verificação, em segundos. Defaults to 0.5.

    Raises:
        Exception: Se ocorrer algum erro inesperado ao verificar o arquivo.

    Returns:
        bool: True se o arquivo foi criado dentro do tempo máximo, False caso contrário.
    """
    try:
        limite = time.monotonic() + tempo_maximo

        while True:
            if os.path.isfile(caminho_arquivo):
                return True

            restante = limite - time.monotonic()
            if restante <= 0:
                return False

            time.sleep(min(intervalo, restante))

    except Exception as error:
        raise Exception(f"Erro inesperado ao aguardar o arquivo '{caminho_arquivo}' | {error}")
