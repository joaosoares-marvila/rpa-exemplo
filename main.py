from src.common.configs import ParametrosExecucaoCompartilhado
from src.processes import executar_processo_1


def main():
    try:
        match ParametrosExecucaoCompartilhado.processo:
            case "1":
                executar_processo_1()

            case _:
                raise Exception(f"Processo {ParametrosExecucaoCompartilhado.processo} não mapeado no RPA Exemplo")
    except Exception as error:
        raise Exception(f"Erro inesperado ao executar RPA Exemplo | {error}")

if __name__ == "__main__":
    main()