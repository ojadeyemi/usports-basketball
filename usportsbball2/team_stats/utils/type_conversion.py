from pandas import DataFrame


def convert_types(df: DataFrame, type_mapping: dict[str, type]) -> DataFrame:
    for column, dtype in type_mapping.items():
        df[column] = df[column].astype(dtype)
    return df
