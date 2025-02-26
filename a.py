import numpy as np

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
            X (numpy.ndarray): 標準化するための 2D データ (形状: [サンプル数, 特徴量数])

        戻り値:
            self (UnbiasedStandardScaler): 学習済みのスケーラーオブジェクト
        """
        X = np.asarray(X)
        self.__mean = X.mean(axis=0)
        self.__std = X.std(axis=0, ddof=1)  # 不偏標準偏差 (n-1 で割る)
        return self

    def transform(self, X):
        """
        学習済みの平均と標準偏差を使用して X を標準化します。

        パラメータ:
            X (numpy.ndarray): 標準化する 2D データ

        戻り値:
            numpy.ndarray: 標準化されたデータ（Zスコア変換後の値）

        例外:
            ValueError: fit() が未実行の場合
        """
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        return (X - self.__mean) / self.__std

    def inverse_transform(self, X_scaled):
        """
        標準化されたデータを元のスケールに戻します。

        パラメータ:
            X_scaled (numpy.ndarray): 標準化済みの 2D データ

        戻り値:
            numpy.ndarray: 元のスケールに戻したデータ

        例外:
            ValueError: fit() が未実行の場合
        """
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        return X_scaled * self.__std + self.__mean

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
    # サンプルデータ
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # スケーラーのインスタンス化
    scaler = UnbiasedStandardScaler()

    # 学習
    scaler.fit(X)

    # 平均と標準偏差の取得（外部から変更不可）
    print("Mean:", scaler.get_mean())  # [4. 5. 6.]
    print("Std (Unbiased):", scaler.get_std())  # [3. 3. 3.]

    # 標準化
    X_scaled = scaler.transform(X)
    print("標準化後のデータ:\n", X_scaled)

    # 逆変換
    X_restored = scaler.inverse_transform(X_scaled)
    print("逆変換後のデータ（元のスケール）:\n", X_restored)
