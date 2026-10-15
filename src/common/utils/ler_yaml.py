import yaml


def ler_yaml(caminho_arquivo: str) -> dict:
    """
    Lê um arquivo YAML e retorna seu conteúdo como um dicionário.

    Args:
        caminho_arquivo (str): O caminho para o arquivo YAML.

    Returns:
        dict: O conteúdo do arquivo YAML como um dicionário.
    """
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = yaml.safe_load(arquivo)
        return conteudo
    
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
    
    except yaml.YAMLError as yaml_error:
        raise yaml.YAMLError(f"Erro ao ler o arquivo YAML | {yaml_error}")
    
    except Exception as error:
        raise Exception(f"Erro inesperado ao ler o arquivo YAML | {error}")