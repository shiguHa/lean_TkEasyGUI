import configparser
import os
from gui import BayesianOptimizationApp

# if __name__ == "__main__":
#     app = BayesianOptimizationApp()
#     app.run()


def read_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {file_path}")
    config = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as file:
        config.read_file(file)
    return config

def get_password(config):
    # 環境変数のキーが設定されている場合は環境変数から取得
    if 'password_env' in config['Database'] and config['Database']['password_env'].strip():
        password_env_key = config['Database']['password_env']
        password = os.getenv(password_env_key)
        if password is None:
            raise ValueError(f"{password_env_key} 環境変数が設定されていません")
        return password
    # それ以外の場合は平文のパスワードを取得
    return config['Database']['password']

# 設定ファイルを読み込む例
config = read_config('config.ini')
db_host = config['Database']['host']
db_port = config.getint('Database', 'port')
db_user = config['Database']['user']
db_password = get_password(config)
db_name = config['Database']['database']

print(f"DB Host: {db_host}")
print(f"DB Port: {db_port}")
print(f"DB User: {db_user}")
print(f"DB Password: {db_password}")
print(f"DB Name: {db_name}")

# https://qiita.com/__Kat__/items/a8db248b075a6ce2efc2
# https://github.com/issp-center-dev/PHYSBO
# https://www.pasj.jp/web_publish/pasj2021/proceedings/PDF/WEOB/WEOB03_oral.pdf