from src.common.configs import ParametrosExecucaoCompartilhado
from src.processes import executar_processo_1, executar_processo_2


def main():
    """ Executa o processo do RPA Exemplo definido pela variável de ambiente `processo`.

    Raises:
        Exception: Se o processo não estiver mapeado ou ocorrer algum erro durante a execução, uma exceção será lançada com a mensagem de erro.
    """
    try:
        match ParametrosExecucaoCompartilhado.processo:
            case "1":
                executar_processo_1()

            case "2":
                executar_processo_2()

            case _:
                raise Exception(f"Processo {ParametrosExecucaoCompartilhado.processo} não mapeado no RPA Exemplo")
    except Exception as error:
        raise Exception(f"Erro inesperado ao executar RPA Exemplo | {error}")

if __name__ == "__main__":
    main()