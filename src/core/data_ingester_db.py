from pathlib import Path
from src.clients.db_client import DBClient
import glob
import pandas as pd
from typing import List


def _filter_out_file_names(file_name: str) -> bool:
    return "expenses" not in file_name


def _identify_number_signal_and_cast_float(series: pd.Series) -> pd.Series:
    # identify if the number is positive or negative
    series = series.apply(lambda x: -x if x[-1] == "D" else x)
    # removing letter at the end and casting to float
    return series.apply(lambda x: float(x[:-1]))
     

def _get_files_list() -> List[str]:
    desktop_path = Path(__file__).resolve().parents[5]
    files_local_storage_path = f"{desktop_path}/personal_app_financial_data_producer/storage/financial_data"

    files_list = glob.glob(f"{files_local_storage_path}/*.json")

    files_list = filter(_filter_out_file_names, files_list)
    
    return list(files_list)


def _generate_and_append_dfs(files_list: List[str],
                             df: pd.DataFrame) -> pd.DataFrame:
    
    for file in files_list:
        df_aux = pd.read_json(file)
        df = df.append(df_aux, ignore_index=True)
    
    return df

files_list = _get_files_list()
df = _generate_and_append_dfs(files_list=files_list,
                              df=pd.DataFrame())

df.balance_value = _identify_number_signal_and_cast_float(series=df.balance_value)
db = DBClient(db_name="financial")

df.to_sql(
        name="balance",
        con=db.engine,
        schema="personal_finances",
        if_exists="append",
        index=False,
        chunksize=16383
        )

db.cnn.close()
db.cursor.close()
