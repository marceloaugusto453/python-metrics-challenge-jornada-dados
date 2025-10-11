import os
import sys
from src.reader import carregar_csv
from src.schema import validar_e_separar
from src.transform import calcular_bonus, gerar_relatorio_individual
from src.kpis import gerar_kpis


from loguru import logger
from datetime import datetime

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"etl_{timestamp}.log")

    logger.remove()  
    logger.add(sys.stderr, level="INFO")
    logger.add(log_file, 
               rotation="10 MB", 
               retention="10 days", 
               level="INFO",
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}")
    
    logger.info("Configuração de log realizada com sucesso.")


if __name__ == "__main__":
    setup_logging() 
    logger.info("Pipeline ETL do funcionário iniciada")
    
    df = carregar_csv("data/funcionarios.csv")

    df_validos, df_invalidos = validar_e_separar(df, "output/erros.csv")

    df_com_bonus = calcular_bonus(df_validos)

    gerar_relatorio_individual(df_com_bonus, "output/relatorio_individual.csv")
    kpis = gerar_kpis(df_com_bonus, "output/kpis.json")

    print("KPIs:", kpis)

    logger.info("Pipeline ETL finalizada com sucesso")