import numpy as np
import pandas as pd



def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # log returns
    df['LR_1D'] = np.log(df['close'] / df['close'].shift(1))
    df['LR_7D'] = np.log(df['close'] / df['close'].shift(7))

    # momentum
    df['M_14D'] = df['close'] / df['close'].shift(14) - 1

    # realized vol
    df['V_7D'] = df["LR_1D"].rolling(7).std()
    df['V_30D'] = df["LR_1D"].rolling(30).std()

    return df




def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['V_1D'] = df['volume'] - df['volume'].shift(1)
    df['V_7D'] = df['volume'].rolling(7).mean()

    # turnover proxy: volume / circulating (circulating not available via Alpaca) — keep as naive
    df['T_7D'] = df['volume'] / df['volume'].rolling(7).mean()
    return df




def make_target(df: pd.DataFrame, horizon=1):
    df = df.copy()
    df['FWD_RET'] = df['close'].shift(-horizon) / df['close'] - 1
    df['TARGET'] = (df["FWD_RET"] > 0).astype(int)
    return df
