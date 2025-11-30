import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import lightgbm as lgb


FEATURES = [
    'LR_1D',
    'LR_7D',
    'M_14D',
    'V_30D',
    'V_1D',
    'V_7D'
]


class Model:
    def __init__(self):
        self.model = None


    def fit(self, df):
        X = df[FEATURES]
        y = df['TARGET']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)


        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test)


        params = {
        'objective': 'binary',
        'metric': 'auc',
        'learning_rate': 0.05,
        'num_leaves': 31,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5
        }


        self.model = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=500)


        preds = self.predict_proba(X_test)
        auc = roc_auc_score(y_test, preds)
        return {'auc': auc}


    def predict_proba(self, X):
        return self.model.predict(X)







class Backtester:
    def __init__(self, df):
        self.df = df.copy()


    def run(self, signal_col='signal'):
        df = self.df.copy()
        # naive sizing: 1 unit when signal==1 else 0
        df['position'] = df[signal_col].shift(1).fillna(0) # use yesterday's signal
        df['strategy_ret'] = df['position'] * df['FWD_RET']
        df['cum_strategy'] = (1 + df['strategy_ret']).cumprod()
        df['cum_benchmark'] = (1 + df['FWD_RET']).cumprod()
        return df

