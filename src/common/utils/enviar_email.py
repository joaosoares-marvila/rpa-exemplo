import mimetypes
import os
import smtplib
from email.message import EmailMessage

from loguru import logger


def enviar_email(
    servidor: str,
    porta: int,
    remetente: str,
    senha: str,
    destinatarios: list[str],
    assunto: str,
    corpo: str,
    anexos: list[str] = None,
    habilitado: bool = False,
) -> None:
    """ Envia um e-mail através de um servidor SMTP com STARTTLS e autenticação.

    Args:
        servidor (str): Endereço do servidor SMTP.
        porta (int): Porta do servidor SMTP (ex.: 587 para STARTTLS).
        remetente (str): Endereço de e-mail usado para autenticar e como remetente.
        senha (str): Senha de autenticação no servidor SMTP.
        destinatarios (list[str]): Lista de e-mails que receberão a mensagem.
        assunto (str): Assunto do e-mail.
        corpo (str): Texto do corpo do e-mail.
        anexos (list[str], optional): Caminhos completos dos arquivos que serão anexados. Defaults to None.
        habilitado (bool, optional): Quando False, o e-mail não é enviado e apenas um alerta é registrado. Defaults to False.

    Raises:
        FileNotFoundError: Se algum dos anexos não existir.
        Exception: Se ocorrer algum erro inesperado ao enviar o e-mail.
    """
    if not habilitado:
        logger.warning(f"Envio de e-mail desabilitado. O e-mail '{assunto}' não será enviado.")
        return

    try:
        mensagem = EmailMessage()
        mensagem["From"] = remetente
        mensagem["To"] = ", ".join(destinatarios)
        mensagem["Subject"] = assunto
        mensagem.set_content(corpo)

        for caminho_anexo in anexos or []:
            if not os.path.isfile(caminho_anexo):
                raise FileNotFoundError(f"O anexo '{caminho_anexo}' não foi encontrado.")

            tipo, _ = mimetypes.guess_type(caminho_anexo)
            tipo_principal, subtipo = (tipo or "application/octet-stream").split("/", 1)

            with open(caminho_anexo, "rb") as arquivo:
                mensagem.add_attachment(
                    arquivo.read(),
                    maintype=tipo_principal,
                    subtype=subtipo,
                    filename=os.path.basename(caminho_anexo),
                )

        with smtplib.SMTP(servidor, porta, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha)
            smtp.send_message(mensagem)

        logger.info(f"E-mail '{assunto}' enviado para {len(destinatarios)} destinatário(s).")

    except FileNotFoundError:
        raise

    except Exception as error:
        raise Exception(f"Erro inesperado ao enviar o e-mail '{assunto}' | {error}")
