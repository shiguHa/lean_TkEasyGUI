import numpy as np
import pandas as pd

class UnbiasedStandardScaler:
    """
    Unbiased Standard Scaler (不偏標準化スケーラー)
    
    各特徴量（列）ごとに平均を引き、不偏標準偏差（n-1で割る）でスケーリングします。
    fit() で学習し、transform() で標準化を適用、inverse_transform() で元のスケールに戻せます。

    属性:
        __mean (numpy.ndarray): 各列の平均値（外部から変更不可）
        __std (numpy.ndarray): 各列の不偏標準偏差（外部から変更不可）
    """

    def __init__(self):
        """UnbiasedStandardScaler のインスタンスを初期化"""
        self.__mean = None  # 平均（外部から変更不可）
        self.__std = None   # 不偏標準偏差（外部から変更不可）

    def fit(self, X):
        """
        データ X を学習し、各列ごとの平均と不偏標準偏差を計算します。

        パラメータ:
            X (numpy.ndarray or pandas.DataFrame): 標準化するための 2D データ (形状: [サンプル数, 特徴量数])

        戻り値:
            self (UnbiasedStandardScaler): 学習済みのスケーラーオブジェクト
        """
        # Pandas DataFrame が渡された場合、numpy 配列に変換
        X = np.asarray(X)
        self.__mean = X.mean(axis=0)
        self.__std = X.std(axis=0, ddof=1)  # 不偏標準偏差 (n-1 で割る)
        return self

    def transform(self, X):
        """
        学習済みの平均と標準偏差を使用して X を標準化します。

        パラメータ:
            X (numpy.ndarray or pandas.DataFrame): 標準化する 2D データ

        戻り値:
            numpy.ndarray: 標準化されたデータ（Zスコア変換後の値）
        """
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        
        # 標準化の計算
        X = np.asarray(X)
        X_scaled = (X - self.__mean) / self.__std
        
        # 結果は常に numpy.ndarray として返す
        return X_scaled

    def inverse_transform(self, X_scaled):
        """
        標準化されたデータを元のスケールに戻します。

        パラメータ:
            X_scaled (numpy.ndarray): 標準化済みの 2D データ

        戻り値:
            numpy.ndarray: 元のスケールに戻したデータ
        """
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        
        # 元のスケールに戻す
        X_restored = X_scaled * self.__std + self.__mean
        return X_restored

    def get_mean(self):
        """
        学習済みの各列の平均値を取得します。

        戻り値:
            numpy.ndarray: 各列の平均値（コピーを返すため、外部から変更不可）
        """
        return self.__mean.copy() if self.__mean is not None else None

    def get_std(self):
        """
        学習済みの各列の不偏標準偏差を取得します。

        戻り値:
            numpy.ndarray: 各列の不偏標準偏差（コピーを返すため、外部から変更不可）
        """
        return self.__std.copy() if self.__std is not None else None


# --- 使用例 ---
if __name__ == "__main__":
    # Pandas DataFrame を使用したサンプルデータ
    df = pd.DataFrame({
        'A': [1, 4, 7],
        'B': [2, 5, 8],
        'C': [3, 6, 9]
    })

    # スケーラーのインスタンス化
    scaler = UnbiasedStandardScaler()

    # 学習
    scaler.fit(df)

    # 平均と標準偏差の取得（外部から変更不可）
    print("Mean:", scaler.get_mean())  # [4. 5. 6.]
    print("Std (Unbiased):", scaler.get_std())  # [3. 3. 3.]

    # 標準化
    df_scaled = scaler.transform(df)
    print(type(df_scaled))
    print("標準化後のデータ:\n", df_scaled)

    # 逆変換
    df_restored = scaler.inverse_transform(df_scaled)
    print("逆変換後のデータ（元のスケール）:\n", df_restored)
