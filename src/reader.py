import pandas as pd

def carregar_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["salario"] = pd.to_numeric(df["salario"], errors="coerce")
    df["bonus_percentual"] = pd.to_numeric(df["bonus_percentual"], errors="coerce")
    return df
