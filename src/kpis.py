import json
import pandas as pd

def gerar_kpis(df_validos: pd.DataFrame, path_saida: str = "output/kpis.json"):
    """Calcula métricas e exporta em JSON"""

    qtd_por_area = df_validos.groupby("area")["id"].count().to_dict()
    media_salario_por_area = df_validos.groupby("area")["salario"].mean().round(2).to_dict()
    bonus_total = round(df_validos["bonus_final"].sum(), 2)

    top3_bonus = (
        df_validos.nlargest(3, "bonus_final")[["nome", "bonus_final"]]
        .to_dict(orient="records")
    )

    kpis = {
        "quantidade_funcionarios_por_area": qtd_por_area,
        "media_salario_por_area": media_salario_por_area,
        "bonus_total_geral": bonus_total,
        "top3_bonus": top3_bonus,
    }

    with open(path_saida, "w", encoding="utf-8") as f:
        json.dump(kpis, f, ensure_ascii=False, indent=4)

    return kpis
