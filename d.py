import configparser
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import ResultProxy
from typing import List, Callable, Any
import pandas as pd
import logging

class Database:
    def __init__(self, config_path='config.ini'):
        self.config = self.read_config(config_path)
        self.engine = self.create_engine()
        self.setup_logging()

    def read_config(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"設定ファイルが見つかりません: {file_path}")
        config = configparser.ConfigParser()
        with open(file_path, 'r', encoding='utf-8') as file:
            config.read_file(file)
        return config

    def get_password(self):
        if 'password_env' in self.config['Database'] and self.config['Database']['password_env'].strip():
            password_env_key = self.config['Database']['password_env']
            password = os.getenv(password_env_key)
            if password is None:
                raise ValueError(f"{password_env_key} 環境変数が設定されていません")
            return password
        return self.config['Database']['password']

    def create_engine(self):
        db_host = self.config['Database']['host']
        db_port = self.config.getint('Database', 'port')
        db_user = self.config['Database']['user']
        db_password = self.get_password()
        db_name = self.config['Database']['database']
        connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return create_engine(connection_string, echo=True)

    def setup_logging(self):
        logging.basicConfig(filename='sqlalchemy.log', level=logging.INFO)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def fetch_all(self, query, params=None):
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            return result.fetchall()

    def fetch_one(self, query, params=None):
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            return result.fetchone()

    def fetch_dataframe(self, query, params=None, chunksize=1000):
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            chunks = []
            while True:
                chunk = result.fetchmany(chunksize)
                if not chunk:
                    break
                df_chunk = pd.DataFrame(chunk, columns=result.keys())
                chunks.append(df_chunk)
            return pd.concat(chunks, ignore_index=True)

    def execute(self, query, params=None, confirm_delete=False):
        if "DELETE" in query.upper() and not confirm_delete:
            raise PermissionError("DELETEクエリを実行するにはconfirm_delete=Trueを指定してください。")
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            connection.commit()
            return result.rowcount

    def insert(self, query, params=None):
        return self.execute(query, params)

    def update(self, query, params=None):
        return self.execute(query, params)

    def delete(self, query, params=None, confirm_delete=False):
        return self.execute(query, params, confirm_delete)

    def query(self, sql: str, params: dict, create_entity: Callable[[ResultProxy], Any]) -> List[Any]:
        result = []
        with self.engine.connect() as connection:
            result_proxy = connection.execute(text(sql), params)
            for row in result_proxy:
                result.append(create_entity(row))
        return result

# 使用例
if __name__ == "__main__":
    db = Database()

    # データの取得例
    select_query = "SELECT * FROM your_table"
    df = db.fetch_dataframe(select_query)
    print(df)

    # データの更新例
    update_query = "UPDATE your_table SET column_name = :value WHERE id = :id"
    params = {"value": "new_value", "id": 1}
    affected_rows = db.update(update_query, params)
    print(f"{affected_rows} 行が更新されました。")

    # データの挿入例
    insert_query = "INSERT INTO your_table (column_name) VALUES (:value)"
    params = {"value": "new_value"}
    affected_rows = db.insert(insert_query, params)
    print(f"{affected_rows} 行が挿入されました。")

    # データの削除例（confirm_delete=Trueを指定）
    delete_query = "DELETE FROM your_table WHERE id = :id"
    params = {"id": 1}
    try:
        affected_rows = db.delete(delete_query, params, confirm_delete=True)
        print(f"{affected_rows} 行が削除されました。")
    except PermissionError as e:
        print(e)

    # カスタムエンティティの作成例
    def create_entity(row):
        return {"id": row["id"], "column_name": row["column_name"]}

    custom_query = "SELECT id, column_name FROM your_table"
    entities = db.query(custom_query, {}, create_entity)
    for entity in entities:
        print(entity)