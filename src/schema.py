import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema

AREAS_VALIDAS = ["Vendas", "TI", "Financeiro", "RH", "Operações"]


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
    try:
        df_validado = funcionarios_schema.validate(df, lazy=True)
        return df_validado, pd.DataFrame(columns=df.columns)  

    except pa.errors.SchemaErrors as err:
        idx_invalidos = set(err.failure_cases["index"].tolist())

        df_invalidos = df.loc[df.index.isin(idx_invalidos)].copy()
        df_validos = df.loc[~df.index.isin(idx_invalidos)].copy()

        df_invalidos.to_csv(path_erros, index=False)

        return df_validos, df_invalidos
