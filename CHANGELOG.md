# Changelog

All notable changes to the Diabetes Triage API are documented here.

## v0.2 — Ridge Regression

- **Model change:** Replaced `LinearRegression` with `Ridge(alpha=1.0)`, retaining `StandardScaler`.
- **Reason:** Ridge regression adds L2 regularization, which can help reduce overfitting and improve generalization.
- **Evaluation:** Both versions use the same fixed 80/20 train/test split with `random_state=42`.

| Metric | v0.1 | v0.2 |
|---|---:|---:|
| Model | StandardScaler + LinearRegression | StandardScaler + Ridge |
| Test RMSE | 53.853 | 53.777 |

**Result:** RMSE decreased by 0.076 points, approximately 0.14%. This is a modest improvement on the held-out test split. It supports selecting v0.2 for this assignment, but does not establish clinical effectiveness.

- **Deployment:** Published the versioned Docker image to GitHub Container Registry.
- **Automation:** Added a tag-triggered GitHub Actions workflow to train the version-specific model, build and publish the image, run a container health check, and create a GitHub Release.

## v0.1 — Baseline

- Trained a baseline regression model using `StandardScaler` and `LinearRegression`.
- Evaluated the model on a held-out test split, obtaining an RMSE of 53.853.
- Added the FastAPI `/predict` endpoint for continuous predictions.
- Added the `/health` endpoint for service monitoring.
- Packaged the API and trained model in a Docker image.
- Added GitHub Actions automation for linting, tests, model training, and artifact uploads.

## Limitations

The scikit-learn diabetes dataset is an educational stand-in for clinical data. These predictions are not clinically validated and must not be used to make real patient-care decisions.