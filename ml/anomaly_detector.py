import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURES = [
    "power_kw",
    "temperature",
    "vibration",
    "voltage",
    "current",
]


def train_anomaly_detector(telemetry: pd.DataFrame):
    """
    Train an Isolation Forest model using historical telemetry.
    """

    data = telemetry[FEATURES].dropna()

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )

    model.fit(data)

    return model


def detect_anomalies(model, telemetry: pd.DataFrame):
    """
    Generate anomaly predictions and scores while
    preserving telemetry identifiers.
    """
    data = telemetry.copy()

    features = data[FEATURES].dropna()

    data.loc[features.index, "anomaly_prediction"] = model.predict(
        features[FEATURES]
    )

    data.loc[features.index, "anomaly_score"] = model.decision_function(
        features[FEATURES]
    )

    return data


if __name__ == "__main__":
    print("UrjaIQ anomaly detector module ready.")