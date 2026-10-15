import os
import shutil


def mover_arquivo(caminho_original: str, pasta_destino: str) -> str:
    """ Move um arquivo para uma pasta de destino, criando a pasta caso ela não exista.

    Args:
        caminho_original (str): Caminho completo do arquivo que será movido.
        pasta_destino (str): Pasta para onde o arquivo será movido.

    Raises:
        FileNotFoundError: Se o arquivo original não existir.
        Exception: Se ocorrer algum erro inesperado ao mover o arquivo.

    Returns:
        str: Caminho completo do arquivo após a movimentação.
    """
    try:
        if not os.path.isfile(caminho_original):
            raise FileNotFoundError(f"O arquivo '{caminho_original}' não foi encontrado.")

        os.makedirs(pasta_destino, exist_ok=True)

        caminho_novo = os.path.join(pasta_destino, os.path.basename(caminho_original))
        shutil.move(caminho_original, caminho_novo)

        return caminho_novo

    except FileNotFoundError:
        raise

    except Exception as error:
        raise Exception(f"Erro inesperado ao mover o arquivo '{caminho_original}' | {error}")
