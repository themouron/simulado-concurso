# Sales Analysis Dashboard

Projeto de análise de vendas utilizando Python, PostgreSQL e Power BI.

## Sobre o projeto

Este projeto demonstra um pipeline completo de análise de dados, desde a ingestão de um arquivo CSV até a criação de um dashboard interativo no Power BI.

Fluxo do projeto:

CSV → PostgreSQL → Python (ETL) → Power BI

---

## Tecnologias utilizadas

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Power BI

---

## Estrutura do projeto

```
report-automation-system/
│
├── data/
│   ├── input/
│   │   └── sales_data.csv
│   └── output/
│
├── src/
│   ├── etl.py
│   ├── load_data.py
│   └── sql/
│       ├── create_table.sql
│       └── query.sql
│
├── sales_dashboard.pbix
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Pipeline

### 1. Ingestão

O arquivo CSV é carregado para uma base PostgreSQL utilizando Python.

---

### 2. ETL

Durante a etapa de transformação são realizadas operações como:

- Conversão de datas
- Criação das colunas de mês
- Criação das colunas de dia da semana
- Tradução dos dados para português
- Cálculo do faturamento (Revenue)
- Padronização dos dados

---

### 3. Dashboard

No Power BI foram desenvolvidos indicadores e gráficos para análise das vendas.

KPIs:

- Receita Total
- Quantidade Vendida
- Número de Vendas
- Ticket Médio

Visualizações:

- Receita por mês
- Receita por vendedor
- Receita por região
- Ticket médio por dia da semana
- Produtos vendidos

---

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure a conexão com o PostgreSQL no arquivo `etl.py`.

Execute:

```bash
python src/load_data.py
```

Depois:

```bash
python src/etl.py
```

Abra o arquivo:

```
sales_dashboard.pbix
```

no Power BI Desktop.

---

## Autor

Daniel Mourão