from src.common.utils import ler_yaml


class ParametrosEstaticosProcesso:
    __dados = ler_yaml(r"resources\configs\processo_1.yaml")
    destinatarios_email = __dados["destinatarios_email"]
    diretorio_download = __dados["diretorio_download"]