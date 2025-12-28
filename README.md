# Nintendo Packages ETL

## 📌 Objetivo
Este projeto tem como objetivo aplicar um processo de **ETL (Extract, Transform, Load)** sobre uma base de dados fictícia de pacotes de jogos da Nintendo.  
O foco é demonstrar habilidades em **limpeza, transformação e padronização de dados** utilizando Python e Pandas.

---

## 📂 Estrutura do Projeto
- **Raw Data**: `../Python/data/raw/nintendo_packages.xlsx`  
- **Processed Data**: `../Python/data/processed/nintendo_packages_processed.xlsx`  
- **Notebook**: contém todas as etapas do ETL, com tratamento detalhado de cada coluna.

---

## ⚙️ Etapas do ETL

### 1. Extract
- Leitura do arquivo Excel com `pandas.read_excel`.
- Visualização inicial das dimensões e colunas disponíveis.

### 2. Transform
Tratamento e padronização das colunas:

- **2.1**: Remoção da coluna `Package Id` (não relevante para análise).  
- **2.2**: Substituição de valores inválidos (`---`, `----`, `-----`) por `NaN` e remoção de linhas incompletas.  
- **2.3**: Criação da coluna `Game Console` a partir da coluna `Game`.  
- **2.4**: Ajuste das colunas `Game` (removendo o console do nome) e `Batch` (extraindo apenas o código).  
- **2.5**: Conversão da coluna `Send Date` para o formato brasileiro `DD/MM/YYYY`.  
- **2.6**: Padronização da coluna `Region` (EN → English, PT → Portuguese, JP → Japanese).  
- **2.7**: Renomeação e normalização da coluna `Preço Unit Price` para `Unit Price`, garantindo valores numéricos.  
- **2.8**: Criação da coluna `Total Price` multiplicando `Stock Quantity × Unit Price`.

### 3. Load
- Exportação do dataset final para Excel em `../Python/data/processed/nintendo_packages_processed.xlsx`.

---

## 🧠 Decisões de Design
- Mantive etapas separadas para mostrar ao recrutador **o tratamento aplicado em cada coluna**.  
- Consolidei apenas operações diretamente relacionadas (ex: `Game` + `Batch`), para demonstrar **eficiência sem perder clareza**.  
- Criei funções robustas para normalização de preços e manipulação de strings, mostrando capacidade de lidar com diferentes formatos.  

---

## 📊 Resultado Final
- Dataset inicial: **118 linhas, 12 colunas**  
- Dataset após limpeza e transformação: **109 linhas, 12 colunas**  
- Arquivo final salvo em: `../Python/data/processed/nintendo_packages_processed.xlsx`

---

## 🚀 Como Executar
1. Clone este repositório.  
2. Instale as dependências:
   ```bash
   pip install pandas openpyxl

