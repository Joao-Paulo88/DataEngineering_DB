## **DATABRICKS DATA LAKEHOUSE**

Projeto de Engenharia de Dados, a fim de preparar base de dados para o consumidor final (Analista de Dados/BI).

Realizado na plataforma Databricks, consiste na implementação de um pipeline de ETL responsável por ingerir arquivos no formato CSV armazenados em um Volume, processá-los através da arquitetura medalhão (Bronze, Silver e Gold) e disponibilizar dados confiáveis para consumo analítico. 

---

### **Arquitetura do Projeto:**

Volume (CSV) -> Bronze (Raw Data) -> Silver (Dados Tratados) -> Gold (Dados Agregados / Analíticos)

* **Bronze — Dados Brutos**
  
  Ingestão dos arquivos CSV

  Preservação dos dados originais

  Inclusão de metadados

  Garantia de rastreabilidade

  table: `tb_raw_data`

* **Silver - Dados Tratados**

  Limpeza dos dados

  Conversão de tipos
  
  Padronização

  Remoção de inconsistências

  table: `tb_clean_data`

* **Gold - Dados Analíticos**

  Modelagem Multidimensional (Star Schema)

  Agregações

  Métricas de negócio

  Otimização para consulta
  
  Preparação para dashboards e BI

  table: `tb_fato_vendas`, `tb_dim_carro`, `tb_dim_cliente`, `tb_dim_loja`, `tb_dim_produtos`, `tb_dim_tempo`, `tb_dim_vendedor`

**Modelo Star Schema - Camada Gold**

```
                    ┌─────────────────────┐
                    │   tb_dim_tempo      │
                    │─────────────────────│
                    │ sk_data_venda (PK)  │
                    │ data_venda          │
                    │ ano_venda           │
                    │ mes_venda           │
                    │ dia_venda           │
                    │ semestre_venda      │
                    └──────────┬──────────┘
                               │
     ┌─────────────────────┐   │   ┌─────────────────────┐
     │   tb_dim_cliente    │   │   │   tb_dim_produtos   │
     │─────────────────────│   │   │─────────────────────│
     │ sk_cliente (PK)     │   │   │ sk_produto (PK)     │
     │ cliente_id          │   │   │ produto_peca        │
     │ cliente_nome        │   │   └──────────┬──────────┘
     └──────────┬──────────┘   │              |
                │              │              │
                │              │              │
                └──────────────┼──────────────┘
                               │
                ┌──────────────▼──────────────┐
                │   tb_fato_vendas            │
                │─────────────────────────────│
                │ sk_cliente                  │
                │ sk_produto                  │
                │ sk_carro                    │
                │ sk_vendedor                 │
                │ sk_loja                     │
                │ sk_data_venda               │
                │─────────────────────────────│
                │ IdNotaFiscal                │
                │ valor_unitario              │
                │ quantidade                  │
                │ custo_unitario              │
                │ faturamento (calculated)    │
                │ lucro (calculated)          │
                └──────────────┬──────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
     ┌──────────▼──────────┐   │   ┌──────────▼──────────┐
     │   tb_dim_carro      │   │   │   tb_dim_vendedor   │
     │─────────────────────│   │   │─────────────────────│
     │ sk_carro (PK)       │   │   │ sk_vendedor (PK)    │
     │ marca_carro         │   │   │ vendedor_id         │
     │ modelo_carro        │   │   │ vendedor_nome       │
     └─────────────────────┘   │   └─────────────────────┘
                               │   
                               │                                  
                    ┌──────────▼──────────┐
                    │   tb_dim_loja       │
                    │─────────────────────│
                    │ sk_Loja (PK)        │
                    │ loja_id             │
                    │ loja_nome           │
                    │ grupo_loja          │
                    └─────────────────────┘
```

**Tecnologias utilizadas:**

Databricks: SQL - Apache Spark - Python - Delta Tables - Delta Lake - Unity Catalog - Volumes - Databricks Workflows (Jobs) - Dashboards

**Conceitos Teóricos:**

Data Warehouse - Modelagem Multidimensional - SCD - Data Lake - Data Lakehouse - Arquitetura Medalhão - 5 V's - ETL - ACID Transactions

---

### **Estrutura do Repositório**

```
vendas_pecas_etl/
│
├── README.md                          # Documentação do projeto
│
├── src/                               # Código fonte do projeto
│   │
│   ├── BRONZE/                       # Camada Bronze - Ingestão de dados brutos
│   │   ├── Bronze_PySpark.ipynb        # Implementação em PySpark
│   │   ├── Bronze_SQL.ipynb            # Implementação em SQL
│   │   └── Mover_arquivos.ipynb        # Utilitário para mover arquivos processados
│   │
│   ├── SILVER/                       # Camada Silver - Limpeza e transformação
│   │   ├── Camada_Silver.ipynb         # Implementação em PySpark
│   │   └── Silver_SQL.ipynb            # Implementação em SQL
│   │
│   └── GOLD/                         # Camada Gold - Agregações e modelagem
│       ├── Gold_PySpark.ipynb          # Implementação em PySpark
│       └── Gold_SQL.ipynb              # Implementação em SQL
│
└── utils/                             # Funções utilitárias
    └── defs.py                         # Definições e funções auxiliares
```
---

### **Plano de Execução**

O pipeline é executado automaticamente por um Job no Databricks, responsável por orquestrar as etapas do processo ETL seguindo a arquitetura medalhão.

O fluxo inicia quando um arquivo CSV é disponibilizado no Volume de ingestão (`/Volumes/vendas_pecas/default/my/processar/`). A partir desse momento, o Job executa sequencialmente as tasks responsáveis pelo processamento dos dados.

Recebimento do CSV no diretório

        ↓

Execução do Job

        ↓

Task 1 — Bronze (Ingestão)

        ↓

Task 2 — Silver (Transformação)

        ↓

Task 3 — Mover Arquivos (Controle operacional)

        ↓

Task 4 — Gold (Agregação)

        ↓
Dashboards (Camada de Consumo)