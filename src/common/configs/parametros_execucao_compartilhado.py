import os

from dotenv import load_dotenv

from src.common.schemas import CredenciaisSchema

load_dotenv()

class ParametrosExecucaoCompartilhado:
    processo = os.getenv("processo")
    ambiente_prd = (os.getenv("ambiente_prd", "False").lower() == "true")
    headless = (os.getenv("headless", "False").lower() == "true")
    enviar_email = (os.getenv("enviar_email", "False").lower() == "true")
    credenciais_iprocess_web = CredenciaisSchema(
        login=os.getenv("login_iprocess_web"),
        senha=os.getenv("senha_iprocess_web")
    )
    smtp_servidor = os.getenv("smtp_servidor")
    smtp_porta = int(os.getenv("smtp_porta", "587"))
    credenciais_smtp = CredenciaisSchema(
        login=os.getenv("login_smtp"),
        senha=os.getenv("senha_smtp")
    )