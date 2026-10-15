import os

from dotenv import load_dotenv

from src.common.schemas import CredenciaisSchema

load_dotenv()

class ParametrosExecucaoCompartilhado:
    processo = os.getenv("processo")
    ambiente_prd = (os.getenv("ambiente_prd", "False").lower() == "true")
    headless = (os.getenv("headless", "False").lower() == "true")
    credenciais_iprocess_web = CredenciaisSchema(
        login=os.getenv("login_iprocess_web"),
        senha=os.getenv("senha_iprocess_web")
    )