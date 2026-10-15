import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42

def build_model(version: str):
    if version.startswith("v0.1"):
        return Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])
    return Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=1.0))])  # v0.2: change later

def main(version, out):
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"]); y = Xy.frame["target"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEED)
    model = build_model(version).fit(X_tr, y_tr)
    rmse = float(np.sqrt(mean_squared_error(y_te, model.predict(X_te))))
    out = Path(out); out.mkdir(exist_ok=True, parents=True)
    joblib.dump(model, out / "model.joblib")
    (out / "metrics.json").write_text(json.dumps(
        {"model_version": version, "rmse": rmse, "seed": SEED}, indent=2))
    print(f"{version}: RMSE={rmse:.3f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--version", default="v0.1"); p.add_argument("--out", default="artifacts")
    a = p.parse_args(); main(a.version, a.out)