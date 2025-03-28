import pandas as pd
import numpy as np
from typing import Callable, List, Optional, Tuple

def aggregate_transform(
    df: pd.DataFrame,
    agg_func: Callable[[pd.Series], float],
    group_cols: List[str],
    target_col: str,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    x_range: Optional[Tuple[float, float]] = None,
    y_range: Optional[Tuple[float, float]] = None
) -> pd.Series:
    """
    任意の列でグループ化し、指定の集約関数を適用する汎用関数。

    Parameters:
        df (pd.DataFrame): 入力データフレーム
        agg_func (Callable[[pd.Series], float]): 集約関数（例: np.mean, np.max, geometric_mean）
        group_cols (List[str]): グループ化する列のリスト（例: ['id', 'cnt']）
        target_col (str): 集約する対象の列名（例: 'measure_value'）
        x_col (Optional[str], optional): x の列名（例: 'x'）。デフォルトは None。
        y_col (Optional[str], optional): y の列名（例: 'y'）。デフォルトは None。
        x_range (Optional[Tuple[float, float]], optional): x の範囲 (min, max)。デフォルトは None。
        y_range (Optional[Tuple[float, float]], optional): y の範囲 (min, max)。デフォルトは None。

    Returns:
        pd.Series: 集約した値を各行に適用した Series
    """

    def aggregate(group: pd.DataFrame) -> float:
        filtered = group
        if x_col and x_range:
            filtered = filtered[(filtered[x_col] >= x_range[0]) & (filtered[x_col] <= x_range[1])]
        if y_col and y_range:
            filtered = filtered[(filtered[y_col] >= y_range[0]) & (filtered[y_col] <= y_range[1])]

        if len(filtered) == 0:
            return np.nan  # フィルタ後にデータがない場合は NaN

        return agg_func(filtered[target_col])

    return df.groupby(group_cols)[target_col].transform(lambda x: aggregate(df.loc[x.index]))

# 幾何平均の関数
def geometric_mean(series: pd.Series) -> float:
    return float(np.exp(np.log(series).mean()))

# サンプルデータ
data = {
    'group1': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'group2': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'feature_x': [10, 20, 30, 15, 25, 35, 40, 50, 60],
    'feature_y': [5, 15, 25, 10, 20, 30, 45, 55, 65],
    'value_to_aggregate': [1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
}

df = pd.DataFrame(data)

# 汎用的な引数で集約
df['geo_mean'] = aggregate_transform(
    df,
    geometric_mean,
    group_cols=['group1', 'group2'],
    target_col='value_to_aggregate',
    x_col='feature_x',
    y_col='feature_y',
    x_range=(10, 30),
    y_range=(5, 25)
)

df['arith_mean'] = aggregate_transform(
    df,
    np.mean,
    group_cols=['group1', 'group2'],
    target_col='value_to_aggregate',
    x_col='feature_x',
    y_col='feature_y',
    x_range=(10, 30),
    y_range=(5, 25)
)

df['max_value'] = aggregate_transform(
    df,
    np.max,
    group_cols=['group1', 'group2'],
    target_col='value_to_aggregate',
    x_col='feature_x',
    y_col='feature_y',
    x_range=(10, 30),
    y_range=(5, 25)
)

print(df)
