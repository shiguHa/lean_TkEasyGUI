def export_table_to_csv(engine, table_name, output_dir="output"):
    """
    指定したテーブルをCSVにエクスポートする。

    :param engine: SQLAlchemyのエンジン
    :param table_name: エクスポートするテーブル名
    :param output_dir: CSVの保存先ディレクトリ
    """
    os.makedirs(output_dir, exist_ok=True)  # 出力ディレクトリを作成
    output_file = os.path.join(output_dir, f"{table_name}.csv")

    with engine.connect() as conn:
        with open(output_file, "w", encoding="utf-8") as f:
            conn.connection.cursor().copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", f)

    print(f"Exported {table_name} to {output_file}")

def export_all_tables_to_csv(engine, output_dir="output"):
    """
    データベース内のすべてのテーブルをCSVにエクスポートする。

    :param engine: SQLAlchemyのエンジン
    :param output_dir: CSVの保存先ディレクトリ
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result]

    for table in tables:
        export_table_to_csv(engine, table, output_dir)

    print("All tables exported successfully.")



with engine.connect() as conn:
    with open("output.csv", "wb") as f:
        cur = conn.connection.cursor()
        with cur.copy("COPY upsert.main_table TO STDOUT WITH CSV HEADER") as copy:
            for data in copy:
                f.write(data)

query = """SELECT *
        FROM upsert.main_table
        """
with engine.connect() as conn:
    with open("output.csv", "wb") as f:
        cur = conn.connection.cursor()
        with cur.copy("COPY ({}) TO STDOUT WITH CSV HEADER".format(query)) as copy:
            for data in copy:
                f.write(data)