# CÉLULA 1 — EXTRACT (ler o CSV)

import pandas as pd
entry_path = "../data/raw/SDW2023.csv"
df = pd.read_csv(entry_path)
df.head()

# CÉLULA 2 — TRANSFORM (regra de negócio simples)

def perfil_investidor(saldo):
    if saldo < 2000:
        return "Iniciante"
    elif saldo < 10000:
        return "Intermediário"
    else:
        return "Avançado"

df["Perfil_Investidor"] = df["Balance"].apply(perfil_investidor)
df.head()

## CÉLULA 3 — LOAD (salvar novo CSV)

output_path = "../data/processed/SDW2023_FINAL.csv"
df.to_csv(output_path, index=False)

df = pd.read_csv(output_path)
df.head()
