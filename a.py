import numpy as np

class UnbiasedStandardScaler:
    def __init__(self):
        self.__mean = None  # 平均（外部から変更不可）
        self.__std = None   # 不偏標準偏差（外部から変更不可）

    def fit(self, X):
        """平均と不偏標準偏差を計算"""
        X = np.asarray(X)
        self.__mean = X.mean(axis=0)
        self.__std = X.std(axis=0, ddof=1)  # 不偏標準偏差 (n-1 で割る)
        return self

    def transform(self, X):
        """標準化を適用"""
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        return (X - self.__mean) / self.__std

    def inverse_transform(self, X_scaled):
        """標準化したデータを元のスケールに戻す"""
        if self.__mean is None or self.__std is None:
            raise ValueError("Scaler has not been fitted yet.")
        return X_scaled * self.__std + self.__mean

    def get_mean(self):
        """計算された平均を取得（外部から変更不可）"""
        return self.__mean.copy() if self.__mean is not None else None

    def get_std(self):
        """計算された不偏標準偏差を取得（外部から変更不可）"""
        return self.__std.copy() if self.__std is not None else None

# テスト用のデータ
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
