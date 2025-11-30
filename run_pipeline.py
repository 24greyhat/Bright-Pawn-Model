import pandas as pd
from utils.data import Data
from features import add_price_features, add_volume_features, make_target
import joblib
from utils.config import UNIVERSE
from model import FEATURES
from training import train_and_save




def pipeline(symbol='BTCUSD'):
    fetcher = Data()
    bars = fetcher.fetch_bars(symbol, limit=10000)
    df = bars.copy()
    df = add_price_features(df)
    df = add_volume_features(df)
    df = make_target(df, horizon=1)
    # drop rows with NaNs in features
    df = df.dropna(subset=FEATURES + ['TARGET'])


    # Train and save model
    metrics = train_and_save(df)

    # Load model and predict latest
    clf = joblib.load('models/brightpawn_model.joblib')
    latest = df.iloc[-1:]
    prob = clf.predict_proba(latest[FEATURES])[0]


    print(f"[*] SIGNAL: {round(prob,1)} SYMBOL: {symbol}")





if __name__ == '__main__':
    # run for all symbols in universe
    for s in UNIVERSE:
        try:
            pipeline(symbol=s)
        except Exception as e:
            raise ValueError('Pipeline failed for %s', s)