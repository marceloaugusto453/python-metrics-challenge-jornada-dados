import pandas as pd
import pandera as pa
from loguru import logger
from pandera import Column, Check, DataFrameSchema

AREAS_VALIDAS = ["Vendas", "TI", "Financeiro", "RH", "Operações"]


ERRO_MAP_PANDERA = {
    "not_nullable": "Campos nulos.",
    "is_in": "Campos nulos",
    
    # Erros de Regras
    "str_matches('^[A-Za-zÀ-ÿ\s]+$')": "Nome contém números ou caracteres inválidos.",
    "isin(['Vendas', 'TI', 'Financeiro', 'RH', 'Operações'])": "Área inválida. Deve ser uma das permitidas.",
    "greater_than_or_equal_to(0)": "Salário ou ID deve ser um número positivo ou zero.",
    "between(0, 1, inclusive='both')": "Bônus percentual deve estar entre 0 e 1 (inclusive).",
}

funcionarios_schema = DataFrameSchema(
    {
        "id": Column(int, Check.greater_than_or_equal_to(1), nullable=False),
        "nome": Column(
            str,
            checks=[Check.str_matches(r"^[A-Za-zÀ-ÿ\s]+$")],
            nullable=False,
        ),
        "area": Column(str, checks=[Check.isin(AREAS_VALIDAS)], nullable=False),
        "salario": Column(float, checks=[Check.greater_than_or_equal_to(0)], nullable=False),
        "bonus_percentual": Column(float, checks=[Check.between(0, 1, inclusive="both")], nullable=False),
    },
    strict=True,
)

def validar_e_separar(df: pd.DataFrame, path_erros: str = "output/erros.csv"):
    ''' 
    Função responsável por validar o schema do pandas usando pandera e separar os arquivos entre válidos e não válidos.

    ArgS: Dataframe do Pandas

    Saída: arquivo de output com erros.

    '''

    logger.info("Iniciando transformação: validação de Schema (Pandera).")
    
    try:
        df_validado = funcionarios_schema.validate(df, lazy=True)
        
        logger.success(f"Validação concluída: todos os {len(df_validado)} registros são válidos.")
        
        return df_validado, pd.DataFrame(columns=df.columns.tolist() + ['motivo_erro']) 

    except pa.errors.SchemaErrors as err:
        idx_invalidos = set(err.failure_cases["index"].tolist())
        df_invalidos = df.loc[df.index.isin(idx_invalidos)].copy()
        df_validos = df.loc[~df.index.isin(idx_invalidos)].copy()


        erros_agrupados = (
            err.failure_cases
            ['check'].map(ERRO_MAP_PANDERA).fillna('Erro de Validação Desconhecido') 
            .groupby(err.failure_cases['index'])
            .apply(lambda x: '; '.join(x.astype(str).unique()))
            .rename('motivo_erro')
        )

        df_invalidos = df_invalidos.merge(
            erros_agrupados, 
            left_index=True, 
            right_index=True, 
            how='left'
        )

        df_invalidos['motivo_erro'] = df_invalidos['motivo_erro'].fillna('Erro de Validação Desconhecido')

        erros_contados = df_invalidos['motivo_erro'].value_counts().head(3).to_dict()
        
        logger.info(f"Validação concluída: {len(df_validos)} válidos | {len(df_invalidos)} inválidos.")
        
        logger.info(f"Top 3 motivos de erro: {erros_contados}")

        df_invalidos.to_csv(path_erros, index=False)

        return df_validos, df_invalidos



















