from pathlib import Path

import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor

from epc.passport import read_docx
from epc.predictor import Predictor
from epc.processed.difficulties import difficulties

features = [
    "hours_total",
    "hours_prac",
    "online",
    "difficulty",
    "min_listeners",
    "max_listeners",
]

targets = [
    "taxonomy",
    "positive_reviews",
    "neutral_reviews",
    "negative_reviews",
]


def train_dataframe() -> DataFrame:
    df = pd.read_csv(Path(__file__).parent / "processed" / "pcs.csv", header=0)
    diffs = []
    for diff in list(df["difficulty"]):
        if isinstance(diff, str):
            ds = [difficulties[d] for d in diff.split()]
            diffs.append(int(sum(ds)))
        else:
            diffs.append(next(iter(difficulties.values())))
    df["difficulty"] = diffs
    return df


def prediction_model():
    return RandomForestRegressor(n_estimators=20, random_state=0)


class PassportPredictor(Predictor):
    def classify(self, file_path: Path) -> dict:
        df = train_dataframe()

        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            print(df.to_string())

        passport = read_docx(file_path)

        inputs = [
            [
                passport.hours_cnt,
                passport.hours_prac,
                passport.online,
                difficulties[passport.difficulty],
                passport.min_listeners,
                passport.max_listeners,
            ]
        ]
        return {
            target: prediction_model()
                .fit(df[features], df[target])
                .predict(inputs)
            for target in targets
        }
