import pandas as pd

# ============================================
# CÉLULA 1 — EXTRACT (ler o CSV)
# ============================================

# Definição dos caminhos
file_name = "SDW2023"

# Monta o caminho completo adicionando a extensão .csv
entry_path = f"../data/raw/{file_name}.csv"
output_path = f"../data/processed/{file_name}_FINAL.csv"

try:
    df = pd.read_csv(entry_path)
    print("✅ Arquivo carregado com sucesso!")
    print("Dimensões do dataset:", df.shape)
    print("Colunas disponíveis:", df.columns.tolist())
    
    # Visualização das primeiras linhas
    print("\nPrévia dos dados carregados:")
    print(df.head())   # mostra as 5 primeiras linhas por padrão
except FileNotFoundError:
    print("❌ Arquivo não encontrado. Verifique o caminho.")
except Exception as e:
    print("❌ Erro ao carregar o arquivo:", e)

# ---------------------------
# CÉLULA 2 — TRANSFORM (regra de negócio simples)
# ---------------------------

def perfil_investidor(saldo: float) -> str:
    """
    Classifica o perfil do investidor com base no saldo.
    - < 2000: Iniciante
    - < 10000: Intermediário
    - >= 10000: Avançado
    """
    if pd.isna(saldo):
        return "Saldo Inválido"
    elif saldo < 2000:
        return "Iniciante"
    elif saldo < 10000:
        return "Intermediário"
    else:
        return "Avançado"

# Verifica se a coluna Balance existe
if "Balance" in df.columns:
    df["Perfil_Investidor"] = df["Balance"].apply(perfil_investidor)
    print("✅ Coluna 'Perfil_Investidor' criada com sucesso!")
else:
    print("❌ Coluna 'Balance' não encontrada no dataset.")

# ---------------------------
# CÉLULA 3 — LOAD (salvar novo CSV)
# ---------------------------

try:
    df.to_csv(output_path, index=False)
    print(f"✅ Arquivo salvo em: {output_path}")
except Exception as e:
    print("❌ Erro ao salvar o arquivo:", e)

# Visualização final
print(df.head())
