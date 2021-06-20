import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

from passport_predictor import features, targets, prediction_model, train_dataframe


def run_metrics():
    df = train_dataframe()

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df.to_string())

        l_metrics = []
        for y in targets:
            X_train, X_test, y_train, y_test = train_test_split(
                df[features], df[y], test_size=0.2, random_state=0
            )
            regressor = prediction_model()
            regressor.fit(X_train, y_train)
            y_pred = regressor.predict(X_test)
            l_metrics.append([
                y,
                metrics.mean_absolute_error(y_test, y_pred),
                metrics.mean_squared_error(y_test, y_pred),
                np.sqrt(metrics.mean_squared_error(y_test, y_pred))
            ])

        print(pd.DataFrame(l_metrics, columns=[
            'Feature',
            'Mean Absolute Error',
            'Mean Squared Error',
            'Root Mean Squared Error'
        ]).to_string())


if __name__ == '__main__':
    run_metrics()
