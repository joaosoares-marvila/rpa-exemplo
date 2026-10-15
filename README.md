# RPA Exemplo

Repositório de exemplo de automações (RPA) em Python. Um único ponto de entrada ([main.py](main.py)) executa um de dois processos, escolhido pela variável de ambiente `processo`.

## Processos

| Processo | Resumo | Documentação |
|---|---|---|
| 1 | Baixa o relatório de despesas do portal iProcess Web (ambiente de treinamento), registra cada despesa via navegador, grava o status de cada registro na planilha e envia o relatório por e-mail. | [process_1/README.md](src/processes/process_1/README.md) |
| 2 | Gera CEPs no site Invertexto, consulta cada CEP na API ViaCEP e envia as duas planilhas resultantes por e-mail. | [process_2/README.md](src/processes/process_2/README.md) |

## Sumário

- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Configuração](#configuração)
- [Como executar](#como-executar)
- [Pontos de atenção](#pontos-de-atenção)

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem (`.python-version`, `requires-python`) |
| uv | Gerenciamento de dependências (`pyproject.toml`, `uv.lock`) |
| Selenium | Automação do navegador Chrome |
| requests | Chamadas HTTP (processo 2) |
| pandas + openpyxl | Leitura e escrita de Excel |
| pydantic | Validação e conversão dos dados (schemas) |
| PyYAML | Leitura das configurações de cada processo |
| python-dotenv | Carregamento do `.env` |
| loguru | Logs |

## Arquitetura

```
rpa-exemplo/
├── main.py                              # Ponto de entrada: escolhe o processo a executar
├── resources/
│   └── configs/                         # Modelos (.yaml.example) das configurações de cada processo
└── src/
    ├── common/                          # Código compartilhado entre processos
    │   ├── configs/                     # Parâmetros de execução compartilhados (.env)
    │   ├── schemas/                     # Schemas comuns (credenciais)
    │   └── utils/                       # Driver Chrome, YAML, limpeza de pasta, espera de arquivo, mover arquivo, e-mail, exceções
    └── processes/
        ├── process_1/                   # Registro de despesas (README próprio)
        └── process_2/                   # Geração e consulta de CEPs (README próprio)
```

Cada processo segue a mesma organização interna:

| Pasta/arquivo | Responsabilidade |
|---|---|
| `processo.py` | Orquestração: prepara pastas e driver, chama as tarefas, envia o e-mail e faz a limpeza no `finally`. |
| `tasks/` | Regra de negócio do processo. |
| `apps/` | Integração com sites e APIs. |
| `files/` | Leitura e escrita das planilhas. |
| `schemas/` | Validação e conversão dos dados (pydantic). |
| `configs/` | `ParametrosEstaticosProcesso` (YAML do processo) e `ParametrosExecucaoProcesso` (`.env`, exclusivos do processo). |

Código reutilizável fica em `src/common/utils/`: `obter_driver`, `ler_yaml`, `limpar_pasta`, `aguardar_arquivo_criado`, `mover_arquivo`, `enviar_email` e `RegraNegocioError`.

### Convenções do código

- Um pacote por processo (`src/processes/process_N/`), com `__init__.py` expondo os itens via `__all__`.
- Nomes de classes, métodos e mensagens em português.
- Métodos de automação e de arquivos encapsulam erros e relançam com contexto: `Erro ... | <erro original>`.
- Atributos privados com dupla underscore (`self.__driver`) nas classes de integração.
- Logs com `loguru` em cada etapa relevante.
- Falha em um item de um lote é registrada e o lote segue; falha global interrompe o processo com "Erro crítico e inesperado ao executar o processo N".

### Seleção do processo

- O processo é definido pela variável `processo`. Valores aceitos: `"1"` e `"2"`.
- Qualquer outro valor interrompe a execução com a mensagem "Processo ... não mapeado no RPA Exemplo".

## Configuração

### Variáveis de ambiente (`.env`)

Copie `.env.example` para `.env` e preencha.

Compartilhadas (definidas em [parametros_execucao_compartilhado.py](src/common/configs/parametros_execucao_compartilhado.py)):

| Variável | Obrigatória | Descrição |
|---|---|---|
| `processo` | Sim | Processo a executar: `1` ou `2`. |
| `smtp_servidor` | Sim | Endereço do servidor SMTP usado para enviar o e-mail. |
| `smtp_porta` | Não | Porta do servidor SMTP. Usa STARTTLS. Padrão: `587`. |
| `login_smtp` | Sim | Usuário SMTP. Também é o remetente do e-mail. |
| `senha_smtp` | Sim | Senha do usuário SMTP. |
| `enviar_email` | Não | `true` envia o e-mail ao final do processo. Com `false`, apenas registra um alerta no log. Padrão: `false`. |
| `headless` | Não | `true` executa o Chrome sem interface. Padrão: `false`. |
| `ambiente_prd` | Não | Hoje não é utilizada pelo código. Padrão: `false`. |

Valores booleanos são lidos como texto: use `true` ou `false`.

Variáveis exclusivas de cada processo estão descritas no README do processo: `login_iprocess_web` e `senha_iprocess_web` no [processo 1](src/processes/process_1/README.md#configuração) e `quantidade_ceps` no [processo 2](src/processes/process_2/README.md#configuração).

### Arquivos YAML (`resources/configs/`)

Copie cada `processo_N.yaml.example` para `processo_N.yaml` e preencha. As chaves de cada arquivo estão no README do respectivo processo.

## Como executar

Pré-requisitos:

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- Google Chrome instalado (o Selenium gerencia o driver)

```bash
# 1. Instalar as dependências
uv sync

# 2. Criar os arquivos de configuração a partir dos exemplos
copy .env.example .env
copy resources\configs\processo_1.yaml.example resources\configs\processo_1.yaml
copy resources\configs\processo_2.yaml.example resources\configs\processo_2.yaml

# 3. Preencher .env e os YAMLs, definir `processo` no .env e executar (a partir da raiz do projeto)
uv run main.py
```

## Pontos de atenção

Itens observados no código atual:

- `main.py` importa os dois processos. Por isso, mesmo executando só um deles, os dois YAMLs precisam existir e as variáveis `login_iprocess_web` e `senha_iprocess_web` (processo 1) precisam estar preenchidas, pois são validadas na importação.
- `login_smtp` e `senha_smtp` também são validadas na importação e não podem ser vazias, mesmo com `enviar_email=false`.
- `ambiente_prd` é lido, mas não é usado.
- Os caminhos dos YAMLs são relativos e usam separador Windows (`resources\configs\processo_N.yaml`). Só funcionam se a execução for feita a partir da raiz do projeto.
- O `finally` de cada processo limpa uma pasta antes de fechar o Chrome; se a limpeza lançar erro, `driver.quit()` não é chamado.
- O projeto não possui testes automatizados.
