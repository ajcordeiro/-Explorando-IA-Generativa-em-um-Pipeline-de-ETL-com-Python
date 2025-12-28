
import re
import pandas as pd

# ============================================
# CÉLULA 1 — EXTRACT (ler a base de dados)
# ============================================

# Definição dos caminhos
file_name = "nintendo_packages"

# Monta o caminho completo adicionando a extensão .xlsx
entry_path = f"../Python/data/raw/{file_name}.xlsx"
output_path = f"../Python/data/processed/{file_name}_processed.xlsx"

try:
    df = pd.read_excel(entry_path)
    print("✅ Arquivo carregado com sucesso!")
    print("Dimensões do dataset:", df.shape)
    print("Colunas disponíveis:", df.columns.tolist())

    # Visualização dos dados
    print("\nDados carregados:")

    # Visualização de todos os dados
    # pd.set_option("display.max_rows", None)
    # print(df)

    # Visualização das 5 primeiras linhas
    print(df.head())  # mostra as 5 primeiras linhas

except FileNotFoundError:
    print("❌ Arquivo não encontrado. Verifique o caminho.")
except Exception as e:
    print("❌ Erro ao carregar o arquivo:", e)

# ========================================================================================#

# ------------------------------------------------------
# CÉLULA 2 — TRANSFORM (manipulação dos dados)
# ------------------------------------------------------

# 2.1. Excluir a coluna 'Package Id'

if "Package Id" in df.columns:
    df = df.drop("Package Id", axis=1)

    # Visualização das 5 primeiras linhas
    print("✅ Coluna 'Package Id' removida com sucesso!\n")
    print(df.head())
else:
    print("⚠️ Coluna 'Package Id' não encontrada no dataset.")

# 2.2. Limpeza de valores inválidos e remoção de linhas incompletas

try:
    # Lista de valores inválidos
    invalid_values = ["---", "----", "-----"]

    # Substitui todos os valores inválidos por NaN
    df = df.replace(invalid_values, pd.NA)

    # Agora remove as linhas que ficaram com NaN
    linhas_antes = df.shape[0]
    df = df.dropna(how="any")
    linhas_depois = df.shape[0]

    # Visualizar a prévia
    print(
        f"✅ Limpeza concluída! ({linhas_antes - linhas_depois} linhas removidas.)")
    print("Dimensões após limpeza:", df.shape)

    pd.set_option("display.max_rows", None)

    print("\nPrévia dos dados limpos:")
    print(df.head())
except Exception as e:
    print("❌ Erro na limpeza dos dados:", e)

# 2.3. Criar a coluna "Game Console"

try:
    # Verifica se a coluna existe
    if "Game" in df.columns:
        # Criar coluna "Game Console" (parte depois do "-")
        df["Game Console"] = df["Game"].str.split("-").str[-1].str.strip()

        # Visualizar prévia
        print("✅ Coluna 'Game Console' criada com sucesso!\n")
        print(df[["Game", "Game Console"]].head())

    else:
        print("⚠️ Coluna 'Game' não encontrada no dataset.")
except Exception as e:
    print("❌ Erro ao criar a coluna 'Game Console':", e)

 # 2.4. Ajustar as colunas "Game" e "Batch"

try:
    if "Game" in df.columns:
        # Ajustar coluna "Game" (parte antes do "-")
        df["Game"] = df["Game"].str.split("-").str[0].str.strip()

    if "Batch" in df.columns:
        # Ajustar coluna "Batch" (parte antes do "-")
        df["Batch"] = df["Batch"].str.split("-").str[-1].str.strip()

    print("✅ Colunas 'Game' e 'Batch' ajustadas com sucesso!\n")
    print(df[["Game", "Batch"]].head())
except Exception as e:
    print("❌ Erro ao ajustar colunas 'Game' e 'Batch':", e)

# 2.5. Ajustar a coluna Send Date

try:
    if "Send Date" in df.columns:
        # Converter para datetime e formatar no padrão brasileiro
        df["Send Date"] = pd.to_datetime(
            df["Send Date"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Visualizar prévia
        print("✅ Coluna 'Send Date' convertida para formato brasileiro (DD/MM/YYYY) com sucesso!\n")
        print(df[["Send Date"]].head())
    else:
        print("⚠️ Coluna 'Send Date' não encontrada no dataset.")
except Exception as e:
    print("❌ Erro ao ajustar a coluna 'Send Date':", e)


# 2.6. Ajustar a coluna "Region"

try:
    if "Region" in df.columns:
        # Mapeamento das siglas para nomes completos
        region_map = {
            "EN": "English",
            "PT": "Portuguese",
            "JP": "Japanese"
        }

        # Substituir os valores
        df["Region"] = df["Region"].replace(region_map)

        # Visualizar prévia
        print("✅ Coluna 'Region' ajustada com sucesso!\n")
        print(df[["Region"]].head())
    else:
        print("⚠️ Coluna 'Region' não encontrada no dataset.")
except Exception as e:
    print("❌ Erro ao ajustar a coluna 'Region':", e)

# 2.7. Renomear e ajustar a coluna "Preço Unit Price" para "Unit Price"

try:
    if "Preço Unit Price" in df.columns:
        # 2.7.1. Renomear a coluna
        df = df.rename(columns={"Preço Unit Price": "Unit Price"})
        print("✅ Coluna 'Preço Unit Price' renomeada para 'Unit Price'.")

        # 2.7.2. Função robusta para normalizar string de preço
        def normalize_price(val):
            if pd.isna(val):
                return pd.NA
            s = str(val).strip()

            # Remover tudo que não seja dígito, vírgula, ponto
            s = re.sub(r"[^0-9.,]", "", s)

            # Casos:
            # a) "1.234,56" (pt-BR): ponto milhar, vírgula decimal → remove pontos, vírgula -> ponto
            if "," in s and "." in s:
                # Se a vírgula estiver à direita do último ponto, tratamos como pt-BR
                # Ex: 1.234,56 → remove ".", troca "," por "."
                s = s.replace(".", "").replace(",", ".")
            # b) "50,07" (pt-BR simples): vírgula decimal → troca vírgula por ponto
            elif "," in s and "." not in s:
                s = s.replace(",", ".")
            # c) "1,234.56" (en-US): vírgula milhar, ponto decimal → remove vírgulas
            elif "." in s and "," in s:
                s = s.replace(",", "")

            # d) "1234.56" ou "50" já ok

            try:
                return float(s)
            except:
                return pd.NA

        # 2.7.3. Aplicar normalização
        df["Unit Price"] = df["Unit Price"].apply(normalize_price)

        # 2.7.4. Feedback de conversão
        na_count = df["Unit Price"].isna().sum()
        print("✅ Coluna 'Unit Price' normalizada e convertida para numérico\n")

        print(df[["Unit Price"]].head())

    else:
        print("⚠️ Coluna 'Preço Unit Price' não encontrada no dataset.")
except Exception as e:
    print("❌ Erro ao ajustar a coluna 'Unit Price':", e)

# 2.8. Criar a coluna "Total Price"

try:
    if "Stock Quantity" in df.columns and "Unit Price" in df.columns:
        # Multiplicar quantidade pelo preço unitário
        df["Total Price"] = df["Stock Quantity"].astype(
            float) * df["Unit Price"].astype(float)

        # Visualizar prévia
        print("✅ Coluna 'Total Price' criada com sucesso!\n")
        print(df[["Stock Quantity", "Unit Price", "Total Price"]].head())
    else:
        print("⚠️ Colunas necessárias ('Stock Quantity' e/ou 'Unit Price') não encontradas no dataset.")
except Exception as e:
    print("❌ Erro ao criar a coluna 'Total Price':", e)

# ---------------------------
# CÉLULA 3 — LOAD (salvar o resultado)
# ---------------------------

# Caminho de saída já definido anteriormente:
output_path = f"../Python/data/processed/{file_name}_processed.xlsx"

try:
    df.to_excel(output_path, index=False)
    print(f"✅ Dataset processado salvo com sucesso em: {output_path}")
except Exception as e:
    print("❌ Erro ao salvar o arquivo:", e)
