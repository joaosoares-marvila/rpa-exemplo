# RPA Exemplo – Registro de Despesas no iProcess

Automação (RPA) em Python com dois processos, escolhidos pela variável `processo`:

- **Processo 1:** baixa o relatório de despesas (`expenses.xlsx`) do portal **iProcess Web** (ambiente de treinamento), registra cada despesa no sistema via navegador, grava o status de cada registro de volta na própria planilha e envia o relatório por e-mail.
- **Processo 2:** gera CEPs no site Invertexto, consulta cada CEP na API ViaCEP e envia as duas planilhas resultantes por e-mail.

## Sumário

- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Regras de negócio](#regras-de-negócio)
- [Configuração](#configuração)
- [Como executar](#como-executar)
- [Pontos de atenção](#pontos-de-atenção)

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem (`.python-version`, `requires-python`) |
| uv | Gerenciamento de dependências (`pyproject.toml`, `uv.lock`) |
| Selenium | Automação do navegador Chrome |
| pandas + openpyxl | Leitura e escrita do Excel |
| pydantic | Validação e conversão dos dados (schemas) |
| PyYAML | Leitura das configurações do processo |
| python-dotenv | Carregamento do `.env` |
| loguru | Logs |

## Arquitetura

### Estrutura de diretórios

```
rpa-exemplo/
├── main.py                              # Ponto de entrada: escolhe o processo a executar
├── resources/
│   └── configs/
│       ├── processo_1.yaml.example      # Modelo das configurações do processo 1
│       └── processo_2.yaml.example      # Modelo das configurações do processo 2
└── src/
    ├── common/                          # Código compartilhado entre processos
    │   ├── configs/                     # Parâmetros de execução compartilhados (.env)
    │   ├── schemas/                     # Schemas comuns (credenciais)
    │   └── utils/                       # Driver Chrome, YAML, limpeza de pasta, espera de arquivo, mover arquivo, e-mail, exceções
    └── processes/
        ├── process_1/                   # Processo 1: registro de despesas
        │   ├── processo.py              # Orquestração do processo
        │   ├── apps/                    # Automação da aplicação web (iprocess_web.py)
        │   ├── configs/                 # Parâmetros estáticos (processo_1.yaml) e de execução (.env) do processo 1
        │   ├── files/                   # Leitura/escrita do relatório Excel
        │   ├── schemas/                 # Modelo de uma despesa (DespesaSchema)
        │   └── tasks/                   # Regra de negócio: registrar_despesas
        └── process_2/                   # Processo 2: geração e consulta de CEPs
            ├── processo.py              # Orquestração do processo
            ├── apps/                    # Invertexto (Selenium) e ViaCEP (HTTP)
            ├── configs/                 # Parâmetros estáticos (processo_2.yaml) e de execução (.env) do processo 2
            ├── files/                   # Escrita das planilhas de CEPs
            ├── schemas/                 # CepGeradoSchema e CepConsultadoSchema
            └── tasks/                   # gerar_ceps e consultar_ceps
```

### Processo 2 – Geração e consulta de CEPs

```mermaid
flowchart TD
    A[main.py] -->|processo = 2| B[executar_processo_2]
    B --> C[limpar pasta de saída]
    C --> D[Task 1: gerar N CEPs no Invertexto]
    D --> E[salvar ceps_gerados.xlsx em temp]
    E --> F[Task 2: consultar cada CEP na ViaCEP]
    F --> G[salvar ceps_consultados.xlsx em temp]
    G --> H[mover planilhas para saída]
    H --> I[enviar e-mail com as duas planilhas]
    I --> J[finally: limpar temp e fechar Chrome]
```

- N vem da variável `quantidade_ceps` (padrão `10`, deve ser maior que zero).
- Uma falha ao gerar um CEP é registrada no log e o lote segue. A planilha contém só os CEPs gerados com sucesso.
- Na consulta, cada CEP recebe uma coluna `Status`:
  - `OK`;
  - `CEP não encontrado na ViaCEP`, quando a API retorna `{"erro": "true"}`;
  - `CEP inválido | <cep>`;
  - `Erro inesperado | <detalhe>`.

  Um erro isolado não interrompe o lote.

### Camadas e responsabilidades

| Camada | Arquivo(s) | Responsabilidade |
|---|---|---|
| Entrada | `main.py` | Lê `processo` do ambiente e despacha para o processo correspondente (`match/case`). |
| Orquestração | `processo_1/processo.py` | Cria o driver, faz login, baixa o relatório, lê as despesas, executa a tarefa e faz a limpeza final. |
| Regra de negócio | `processo_1/tasks/registrar_despesas.py` | Percorre as despesas, registra cada uma e atualiza o status na planilha. |
| Aplicação web | `processo_1/apps/iprocess_web.py` | Autenticação, download do relatório e preenchimento do formulário de despesas. |
| Arquivos | `processo_1/files/relatorio_despesas_excel.py` | Converte o Excel em `DespesaSchema` e reescreve linhas com o status. |
| Schemas | `processo_1/schemas/`, `common/schemas/` | Validação e conversão de dados com pydantic. |
| Configuração | `common/configs/`, `processo_N/configs/` | `ParametrosExecucaoCompartilhado` (`.env`, usados por todos os processos), `ParametrosExecucaoProcesso` (`.env`, exclusivos do processo) e `ParametrosEstaticosProcesso` (YAML do processo). |
| Utilitários | `common/utils/` | `obter_driver`, `ler_yaml`, `limpar_pasta`, `aguardar_arquivo_criado`, `mover_arquivo`, `enviar_email`, `RegraNegocioError`. |

### Fluxo de execução

```mermaid
flowchart TD
    A[main.py] -->|processo = 1| B[executar_processo_1]
    B --> B1[limpar pasta de saída]
    B1 --> C[obter_driver: Chrome]
    C --> D[IprocessWeb: login]
    D --> E[baixar_relatorio_despesas]
    E --> F[RelatorioDespesasExcel.ler]
    F --> G{Para cada despesa}
    G --> H[registrar_despesa no iProcess]
    H --> I[atualizar_status na planilha]
    I --> G
    G -->|fim| G1[mover relatório para saída]
    G1 --> G2[enviar e-mail com o relatório]
    G2 --> J[finally: limpar pasta de download e fechar Chrome]
```

### Convenções do código

- Um pacote por processo (`src/processes/process_N/`), com `__init__.py` expondo os itens via `__all__`.
- Nomes de classes, métodos e mensagens em português.
- Métodos de automação e de arquivos encapsulam erros e relançam com contexto: `Erro ... | <erro original>`.
- Atributos privados com dupla underscore (`self.__driver`) nas classes de integração.
- Logs com `loguru` em cada etapa relevante.

## Regras de negócio

### Seleção do processo

- O processo é definido pela variável `processo`. Valores aceitos: `"1"` e `"2"`.
- Qualquer outro valor interrompe a execução com a mensagem "Processo ... não mapeado".

### Credenciais

- Processo 1: `login_iprocess_web` e `senha_iprocess_web` são obrigatórios e não podem ser vazios.

### Download do relatório

- O sistema acessa o relatório **Expenses Report** e clica em **Download Expenses Report**.
- O arquivo esperado é `expenses.xlsx`, salvo em `diretorio_download`.
- O processo aguarda até **60 segundos** pelo arquivo. Se não aparecer, a execução é interrompida com erro.

### Leitura e validação das despesas

Todas as colunas são lidas como texto e cada linha é convertida em uma despesa, validada conforme a tabela abaixo.

| Coluna no Excel | Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|---|
| `Id` | `id` | texto | Sim | Não pode ser vazio. |
| `Date` | `data` | data | Não | Aceita `YYYY-MM-DD HH:MM:SS` ou `DD/MM/YYYY`. Vazio vira `None`. |
| `Requester` | `solicitante` | texto | Sim | Não pode ser vazio. |
| `Category` | `categoria` | texto | Sim | Não pode ser vazio. Deve existir na lista de categorias do portal. |
| `Value` | `valor` | decimal | Não definido na validação | Convertido para `Decimal`. |
| `Description` | `descricao` | texto | Não | Vazio vira `None`. |
| `Status` | `status` | texto | Não | Vazio vira `None`. É preenchido pelo processo. |

### Registro de cada despesa

Para cada despesa, o sistema:

1. Abre o formulário **Register Expense**.
2. Preenche Id, Date, Requester, Value e Description.
3. Seleciona a Category pelo texto visível da opção.
4. Se a Description estiver vazia, usa o texto padrão **"Nenhuma descrição fornecida"**.
5. Clica em **Register**.
6. Lê a mensagem de retorno da tela:
   - Se contiver **"Despesa cadastrada com sucesso!"**, o status é `OK`.
   - Caso contrário, o status é `Erro ao registrar despesa | <mensagem da tela>`.

### Tratamento de erros

- **Erro em uma despesa:** o status da linha recebe `Erro inesperado | <detalhe>` e o processamento segue para a próxima despesa. Um erro isolado não interrompe o lote.
- **Erro global** (login, download ou leitura do Excel): o processo é interrompido com a mensagem "Erro crítico e inesperado ao executar o processo 1".

### Atualização da planilha

- Após cada despesa, a linha com o mesmo `Id` (comparado sem espaços nas extremidades) é reescrita com os dados atuais da despesa, incluindo o `Status`.
- Se a coluna `Id` não existir, ou o `Id` não for encontrado, a atualização falha.

### Encerramento

- No início, a pasta `diretorio_saida` é limpa de forma recursiva.
- Ao final do registro, o `expenses.xlsx` com os status gravados é movido para `diretorio_saida` e enviado por e-mail aos `destinatarios_email` (se `enviar_email` for `true`).
- No `finally`, a pasta `diretorio_download` é limpa de forma recursiva e o navegador Chrome é fechado.

## Configuração

### Variáveis de ambiente (`.env`)

Copie `.env.example` para `.env` e preencha:

| Variável | Obrigatória | Descrição |
|---|---|---|
| `processo` | Sim | Processo a executar. Atualmente: `1` ou `2`. |
| `login_iprocess_web` | Sim (processo 1) | Usuário do iProcess Web. Exclusiva do processo 1 (`ParametrosExecucaoProcesso`). |
| `senha_iprocess_web` | Sim (processo 1) | Senha do iProcess Web. Exclusiva do processo 1 (`ParametrosExecucaoProcesso`). |
| `smtp_servidor` | Sim | Endereço do servidor SMTP usado para enviar o e-mail. |
| `smtp_porta` | Não | Porta do servidor SMTP. Usa STARTTLS. Padrão: `587`. |
| `login_smtp` | Sim | Usuário SMTP. Também é o remetente do e-mail. |
| `senha_smtp` | Sim | Senha do usuário SMTP. |
| `enviar_email` | Não | `true` envia o e-mail ao final do processo. Com `false`, apenas registra um alerta no log. Padrão: `false`. |
| `headless` | Não | `true` executa o Chrome sem interface. Padrão: `false`. |
| `quantidade_ceps` | Não | Exclusiva do processo 2 (`ParametrosExecucaoProcesso`): quantidade de CEPs a gerar. Padrão: `10`. |
| `ambiente_prd` | Não | Hoje não é utilizada pelo código. Padrão: `false`. |

Valores booleanos são lidos como texto: use `true` ou `false`.

Os parâmetros compartilhados (`processo`, `ambiente_prd`, `headless`, `enviar_email`, `smtp_*`, `login_smtp`, `senha_smtp`) ficam em [parametros_execucao_compartilhado.py](src/common/configs/parametros_execucao_compartilhado.py). Os exclusivos de cada processo ficam em `parametros_execucao_processo.py`, dentro de [process_1/configs/](src/processes/process_1/configs/) e [process_2/configs/](src/processes/process_2/configs/).

### Configurações do processo 1 (`resources/configs/processo_1.yaml`)

Copie `processo_1.yaml.example` para `processo_1.yaml` e preencha:

| Chave | Descrição |
|---|---|
| `diretorio_download` | Pasta onde o relatório é baixado. Será criada se não existir. É limpa ao final da execução. |
| `diretorio_saida` | Pasta final do relatório. Será criada se não existir. É limpa no início da execução. |
| `destinatarios_email` | Lista de e-mails que recebem o relatório ao final do processo. |

### Configurações do processo 2 (`resources/configs/processo_2.yaml`)

Copie `processo_2.yaml.example` para `processo_2.yaml` e preencha:

| Chave | Descrição |
|---|---|
| `diretorio_temp` | Pasta onde as planilhas são geradas. É limpa ao final da execução. |
| `diretorio_saida` | Pasta final das planilhas. É limpa no início da execução. |
| `destinatarios_email` | Lista de e-mails que recebem as duas planilhas. |

Como `main.py` importa todos os processos, os dois YAMLs precisam existir, mesmo que só um processo seja executado.

## Como executar

Pré-requisitos:

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- Google Chrome instalado (o Selenium gerencia o driver)

Passos:

```bash
# 1. Instalar as dependências
uv sync

# 2. Criar os arquivos de configuração a partir dos exemplos
copy .env.example .env
copy resources\configs\processo_1.yaml.example resources\configs\processo_1.yaml
copy resources\configs\processo_2.yaml.example resources\configs\processo_2.yaml

# 3. Preencher .env e os YAMLs e executar
uv run main.py
```

## Pontos de atenção

Itens observados no código atual:

- `ambiente_prd` é lido, mas não é usado.
- `RegraNegocioError` é importada na tarefa de registro do processo 1, mas nenhuma regra a lança. No processo 2 ela é lançada pela `ViaCepApi`.
- Os caminhos dos YAMLs são relativos e usam separador Windows (`resources\configs\processo_N.yaml`). Só funcionam se o processo for executado a partir da raiz do projeto.
- O projeto não possui testes automatizados.
