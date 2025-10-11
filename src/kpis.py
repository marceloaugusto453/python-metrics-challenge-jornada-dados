import json
import pandas as pd
from loguru import logger

def gerar_kpis(df_validos: pd.DataFrame, path_saida: str = "output/kpis.json"):
    '''
    Função para gerar todos os kpi's a partir do dataframe do pandas. 
    
    KPIS: Qtd. funcionários por área, media de salario por area, bonus total geral e top3 bonus.

    Args: Dataframe: DataFrame contendo apenas registros válidos, 
                     já com os campos 'salario' e 'bonus_percentual' 
                     convertidos para float.

    Output: retorna o data frame e cria o arquivo json no caminho especificado.


    '''

    logger.info("Iniciar geração de KPIs: calculo de metricas agregadas.")

    qtd_por_area = df_validos.groupby("area")["id"].count().to_dict()
    media_salario_por_area = df_validos.groupby("area")["salario"].mean().round(2).to_dict()
    bonus_total = round(df_validos["bonus_final"].sum(), 2)


    top3_bonus = (
        df_validos.nlargest(3, "bonus_final")[["nome", "bonus_final"]]
        .to_dict(orient="records")
    )
    

    logger.info(f"Métrica Principal: Top 3 Bônus Calculados: {top3_bonus}")


    kpis = {
        "quantidade_funcionarios_por_area": qtd_por_area,
        "media_salario_por_area": media_salario_por_area,
        "bonus_total_geral": bonus_total,
        "top3_bonus": top3_bonus,
    }


    try:
        with open(path_saida, "w", encoding="utf-8") as f:
            json.dump(kpis, f, ensure_ascii=False, indent=4)

        logger.success(f"Geração do arquivo finalizada: arquivo salvo em {path_saida}")
        
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo de KPIs em {path_saida}: {e}")

    return kpis