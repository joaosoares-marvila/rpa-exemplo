import os

from dotenv import load_dotenv

load_dotenv()


class ParametrosExecucaoProcesso:
    quantidade_ceps = int(os.getenv("quantidade_ceps") or "10")
