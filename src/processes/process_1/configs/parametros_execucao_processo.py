import os

from dotenv import load_dotenv

from src.common.schemas import CredenciaisSchema

load_dotenv()


class ParametrosExecucaoProcesso:
    credenciais_iprocess_web = CredenciaisSchema(
        login=os.getenv("login_iprocess_web"),
        senha=os.getenv("senha_iprocess_web")
    )
