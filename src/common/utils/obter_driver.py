import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def obter_driver(headless: bool = True, diretorio_download: str = None) -> Chrome:
    """ Obtem o driver do Chrome com as opções especificadas.

    Args:
        headless (bool, optional): Indica se o navegador deve ser executado em modo headless (sem interface gráfica). Defaults to True.
        diretorio_download (str, optional): Caminho da pasta onde os arquivos baixados serão armazenados. Defaults to None.

    Raises:
        Exception: Se ocorrer algum erro inesperado ao obter o driver do Chrome.

    Returns:
        Chrome: Uma instância do driver do Chrome configurada com as opções especificadas.
    """    
    try:
        options = Options()

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-features=PasswordLeakDetection")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }

        if diretorio_download:
            caminho_download = os.path.abspath(diretorio_download)
            os.makedirs(caminho_download, exist_ok=True)
            prefs.update({
                "download.default_directory": caminho_download,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            })

        options.add_experimental_option("prefs", prefs)

        driver = Chrome(options=options)
        if not headless:
            driver.maximize_window()
        return driver

    except Exception as error:
        raise Exception(f"Erro inesperado ao obter o driver do Chrome | {error}")