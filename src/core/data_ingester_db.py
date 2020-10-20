from pathlib import Path
from src.clients.db_client import DBClient
import glob
import pandas as pd


desktop_path = Path(__file__).resolve().parents[5]
files_local_storage_path = f"{desktop_path}/personal_app_financial_data_producer/storage/financial_data"

files_list = glob.glob(f"{files_local_storage_path}/*.json")

def _filter_out_file_names(file_name):
    return "expenses" not in file_name

files_list = filter(_filter_out_file_names, files_list)
files_list = list(files_list)

df = pd.DataFrame()

for file in files_list:
    df_aux = pd.read_json(file)
    df = df.append(df_aux, ignore_index=True)

# identify if the number is positive or negative
df.balance_value = df.balance_value.apply(lambda x: -x if x[-1] == "D" else x)
# removing letter at the end and casting to float
df.balance_value = df.balance_value.apply(lambda x: float(x[:-1]))

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
