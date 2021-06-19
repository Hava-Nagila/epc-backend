from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from epc.passport import read_docx
from epc.predictor import Predictor
from epc.processed.difficulties import difficulties

feats = [
    'hours_total',
    'hours_prac',
    'online',
    'difficulty',
    'min_listeners',
    'max_listeners'
]


def prediction_model():
    return RandomForestRegressor(n_estimators=20, random_state=0)


class PassportPredictor(Predictor):
    def classify(self, file_path: Path) -> dict:
        df = pd.read_csv(Path(__file__) / "processed" / "pcs.csv", header=0)

        df['difficulty'] = df['difficulty'].apply(lambda d: difficulties[d])

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.to_string())

        passport = read_docx(file_path)

        inputs = [[
            passport.hours_cnt,
            passport.hours_prac,
            passport.online,
            difficulties[passport.difficulty],
            passport.min_listeners,
            passport.max_listeners
        ]]
        return {
            target: prediction_model() \
                .fit(df[feats], df[target])
                .predict(inputs)
            for target in [
                'taxonomy',
                'positive_reviews',
                'neutral_reviews',
                'negative_reviews'
            ]
        }
