import pandas as pd

BONUS_BASE = 1000

def calcular_bonus(df_validos: pd.DataFrame) -> pd.DataFrame:
    df_validos = df_validos.copy()
    df_validos["bonus_final"] = BONUS_BASE + df_validos["salario"] * df_validos["bonus_percentual"]
    df_validos["bonus_final"] = df_validos["bonus_final"].round(2)
    return df_validos

def gerar_relatorio_individual(df_validos: pd.DataFrame, path_saida: str = "output/relatorio_individual.csv"):
    df_validos.to_csv(path_saida, index=False)
