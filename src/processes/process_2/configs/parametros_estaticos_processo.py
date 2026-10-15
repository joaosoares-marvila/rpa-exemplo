from src.common.utils import ler_yaml


class ParametrosEstaticosProcesso:
    __dados = ler_yaml(caminho_arquivo=r"resources\configs\processo_2.yaml")
    destinatarios_email = __dados["destinatarios_email"]
    diretorio_temp = __dados["diretorio_temp"]
    diretorio_saida = __dados["diretorio_saida"]
