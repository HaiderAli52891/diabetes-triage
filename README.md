# Diabetes Triage API

A machine learning API that predicts a continuous diabetes disease-progression score using the scikit-learn diabetes dataset. The score can support follow-up prioritization; it is not a diagnosis or a substitute for clinical judgment.

## Model versions

| Version | Model | RMSE |
|---|---|---:|
| v0.1 | StandardScaler + LinearRegression | 53.853 |
| v0.2 | StandardScaler + Ridge Regression (`alpha=1.0`) | 53.777 |

Both versions use the same fixed train/test split (`random_state=42`, test size 20%). The v0.2 model achieves a slightly lower RMSE on this split. This is a small improvement and should not be interpreted as evidence of clinical effectiveness.

## API endpoints

- `GET /health` — health check.
- `POST /predict` — returns a continuous prediction.
- `GET /docs` — interactive API documentation.

### Prediction request

Send a JSON object containing the model's required input features.

Example structure:

```json
{
  "age": 0.05,
  "sex": 0.05,
  "bmi": 0.06,
  "bp": 0.02,
  "s1": -0.04,
  "s2": -0.03,
  "s3": -0.04,
  "s4": -0.01,
  "s5": 0.02,
  "s6": -0.01
}
```

Example response:

```json
{
  "prediction": 151.35
}
```

Invalid requests should return HTTP `422` with validation details.

## Run locally

Python 3.11 is recommended.

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Train the baseline model:

```bash
python src/train.py --version v0.1
```

Train the improved model:

```bash
python src/train.py --version v0.2
```

Training writes `artifacts/model.joblib` and `artifacts/metrics.json`.

Start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

Visit `http://localhost:80/docs` to try the API.

## Run with Docker

Build the image locally:

```bash
docker build -t diabetes-triage:local .
```

Run it:

```bash
docker run --rm -p 8080:80 diabetes-triage:local
```

Check health:

```text
http://localhost:8080/health
```

API documentation:

```text
http://localhost:8080/docs
```

## Published container images

The public images are published to GitHub Container Registry:

- v0.1: `ghcr.io/haiderali52891/diabetes-triage:v0.1`
- v0.2: `ghcr.io/haiderali52891/diabetes-triage:v0.2`

Pull a version:

```bash
docker pull ghcr.io/haiderali52891/diabetes-triage:v0.2
```

Run it:

```bash
docker run --rm -p 8080:80 ghcr.io/haiderali52891/diabetes-triage:v0.2
```

The v0.2 image will be available after its release workflow succeeds.

## Testing and CI/CD

GitHub Actions runs linting, tests, and a model-training smoke test on pushes to `main` and pull requests targeting `main`. Training artifacts are uploaded by the workflow.

A separate release workflow builds and publishes a Docker image when a version tag matching `v*` is pushed, checks the container's health endpoint, and creates a GitHub Release.

## Changelog

### v0.2
- Changed the estimator from LinearRegression to Ridge regression (`alpha=1.0`).
- RMSE decreased from 53.853 to 53.777 on the fixed test split.

### v0.1
- Initial baseline using StandardScaler and LinearRegression.
- FastAPI prediction and health endpoints.
- Docker packaging and automated CI.

## Limitations

This is an educational machine learning project using the scikit-learn diabetes dataset. Its predictions are not validated for clinical use and must not be used as the sole basis for medical decisions.