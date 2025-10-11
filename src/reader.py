import pandas as pd
from loguru import logger

def carregar_csv(path: str) -> pd.DataFrame:
    '''
    Função responsável por fazer a leitura do arquivo CSV.

    Args: caminho do arquivo

    Saída: retorna uma dataframe do pandas.
    '''

    logger.info(f"Iniciando extração: lendo arquivo CSV em: {path}")

    try:
        df = pd.read_csv(path)
        df["salario"] = pd.to_numeric(df["salario"], errors="coerce")
        df["bonus_percentual"] = pd.to_numeric(df["bonus_percentual"], errors="coerce")

        total_linhas = len(df)
        logger.success(f"Extração realizada: arquivo {path} lido com sucesso.")
        logger.info(f"Metrica | Total de linhas lidas: {total_linhas}")

        return df
    
    except FileNotFoundError:
        logger.error(f"Erro ao ler o arquivo: arquivo não encontrado no caminho: {path}")
        return pd.DataFrame()
    except Exception as e:
        logger.exception(f"Erro ao carregar o CSV {e}")
        return pd.DataFrame()    