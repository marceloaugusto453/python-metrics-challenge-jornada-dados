# src/writer.py (Melhorado)

import pandas as pd
from loguru import logger

def gerar_relatorio_individual(df_validos: pd.DataFrame, path_saida: str = "output/relatorio_individual.csv"):
    """
    Salva os registros válidos com o bônus calculado.
    
    """
    logger.info(f"Iniciando load: Salvando relatório individual em {path_saida}")
    
    try:
        df_validos.to_csv(path_saida, index=False)
        
        linhas_gravadas = len(df_validos)
        logger.success(f"Load concluído: relatório individual gerado em '{path_saida}' com {linhas_gravadas} linhas.")
    
    except Exception as e:
        logger.error(f"Erro ao gerar o relatorio_individual.csv {path_saida}: {e}")