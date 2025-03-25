import pandas as pd
import numpy as np

def aggregate_transform(df, agg_func, x_range=None, y_range=None):
    """
    id, cnt ごとの measure_value の集計を行い、transform で適用する汎用関数。

    Parameters:
        df (pd.DataFrame): 入力データフレーム
        agg_func (callable): 集約関数（例: np.mean, np.max, geometric_mean）
        x_range (tuple, optional): x の範囲 (min, max) 
        y_range (tuple, optional): y の範囲 (min, max) 

    Returns:
        pd.Series: 集約した値を各行に適用した Series
    """
    def aggregate(group):
        filtered = group
        if x_range:
            filtered = filtered[(filtered['x'] >= x_range[0]) & (filtered['x'] <= x_range[1])]
        if y_range:
            filtered = filtered[(filtered['y'] >= y_range[0]) & (filtered['y'] <= y_range[1])]

        if len(filtered) == 0:
            return np.nan  # フィルタ後にデータがない場合は NaN

        return agg_func(filtered['measure_value'])

    return df.groupby(['id', 'cnt'])['measure_value'].transform(lambda x: aggregate(df.loc[x.index]))

# 幾何平均の関数
def geometric_mean(series):
    return np.exp(np.log(series).mean())

# サンプルデータ
data = {
    'id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'cnt': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'x': [10, 20, 30, 15, 25, 35, 40, 50, 60],
    'y': [5, 15, 25, 10, 20, 30, 45, 55, 65],
    'measure_value': [1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
}

df = pd.DataFrame(data)

# 各集計方法の適用
df['geo_mean'] = aggregate_transform(df, geometric_mean, x_range=(10, 30), y_range=(5, 25))
df['arith_mean'] = aggregate_transform(df, np.mean, x_range=(10, 30), y_range=(5, 25))
df['max_value'] = aggregate_transform(df, np.max, x_range=(10, 30), y_range=(5, 25))

print(df)
