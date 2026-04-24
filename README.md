# 🎬 CineMatch — Scalable Movie Recommendation System

> A production-ready, content-based movie recommendation engine powered by FastAPI, deployed on AWS via a fully automated CI/CD pipeline.

## 🌐 Live Demo

**👉 [http://18.118.149.202:8000/](http://18.118.149.202:8000/)**

> Hosted on AWS EC2 — select any movie and get instant recommendations with posters.

---

## 📖 Overview

CineMatch is an end-to-end ML system that recommends movies similar to a user's selection using a precomputed cosine similarity matrix. The system exposes a REST API built with FastAPI, integrates with the TMDB API for real-time poster fetching, and is deployed on AWS EC2 via Docker — with zero manual deployment steps thanks to a GitHub Actions CI/CD pipeline.

This is not a notebook experiment. It is a production-grade ML system designed for reliability, portability, and scalability.

---

## 🧠 Problem Statement

Given a movie title selected by a user, the system must return the top 5 most similar movies along with their posters — in real time. The challenge is to serve recommendations with low latency while keeping the infrastructure lightweight, reproducible, and automatically deployable.

---

## 🏗️ System Architecture

```
User (Browser)
      │
      ▼
FastAPI Backend (Uvicorn / Port 8000)
      │
      ├── GET  /          → Serves frontend UI (HTML)
      ├── GET  /movies    → Returns full movie list from pickle
      └── POST /recommend → Runs similarity inference → fetches posters → returns results
                │
                ├── Loads precomputed similarity matrix (pickle)
                ├── Finds top-5 similar movie indices
                └── Calls TMDB API for each poster URL
```

**Artifact Layer:**
Model pickle files are stored in AWS S3 and downloaded into the Docker image at build time during the CI/CD pipeline — keeping them out of Git while ensuring they are baked into the deployed container.

**Deployment Pipeline:**
```
Git Push → GitHub Actions CI
               → Lint + Test
               → Download artifacts from S3
               → Docker Build + Push to ECR
               → EC2 Pull + Run Container
```

---

## ⚙️ How It Works

1. At startup, the app loads two pickle files: a movie dataframe and a precomputed cosine similarity matrix.
2. When a user selects a movie and clicks Recommend, the frontend POSTs the movie title to `/recommend`.
3. The backend looks up the movie's index in the dataframe and retrieves its similarity scores from the matrix.
4. The scores are sorted in descending order and the top 5 results (excluding the input movie itself) are selected.
5. For each result, the TMDB API is called using the movie's ID to fetch the poster URL.
6. The response is returned as a JSON array of title + poster pairs and rendered in the UI.

---

## 🛠️ Tech Stack

**ML / Data**
- scikit-learn — cosine similarity computation
- pandas — movie dataframe operations
- pickle — model artifact serialization

**Backend**
- FastAPI — REST API framework
- Uvicorn — ASGI server
- Pydantic — request validation
- Requests — TMDB API integration

**DevOps / MLOps**
- Docker — containerization
- GitHub Actions — CI/CD pipeline
- AWS S3 — artifact storage
- AWS ECR — container registry

**Cloud**
- AWS EC2 — self-hosted runner + application server

---

## 📡 API Endpoints

### `GET /`
Serves the frontend HTML UI.

---

### `GET /movies`
Returns the full list of available movie titles.

**Response:**
```json
{
  "movies": ["The Dark Knight", "Inception", "Interstellar", "..."]
}
```

---

### `POST /recommend`
Runs inference and returns top 5 similar movies with poster URLs.

**Request:**
```json
{
  "data": "Inception"
}
```

**Response:**
```json
{
  "recommendation": [
    { "title": "The Dark Knight", "poster": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Interstellar",    "poster": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Memento",         "poster": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Shutter Island",  "poster": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "The Prestige",    "poster": "https://image.tmdb.org/t/p/w500/..." }
  ]
}
```

**Error Responses:**
- `404` — Movie not found in database
- `500` — Missing column or internal server error

---

## 📊 ML Approach

**Type:** Content-based filtering

**Method:** Precomputed cosine similarity matrix over movie feature vectors (likely built from genre, cast, keywords, and overview data).

**Why precomputation?**
Computing similarity at request time for thousands of movies would be too slow for a real-time API. By precomputing the full N×N similarity matrix offline and loading it at startup, every recommendation query is reduced to a single array lookup and sort — making inference essentially instant regardless of dataset size.

**Artifacts:**
- `movie_df.pkl` — Pandas DataFrame with movie metadata (title, id, etc.)
- `similarity_data.pkl` — Precomputed cosine similarity matrix (N×N float array)

---

## 🚀 Deployment & MLOps

### CI — Continuous Integration (GitHub-hosted runner)
- Checks out code from `main` branch
- Sets up Python environment
- Installs dependencies from `requirements.txt`
- Lints with `flake8` (hard errors block the pipeline; style warnings do not)
- Runs `pytest` (non-blocking)

### CD — Continuous Delivery (GitHub-hosted runner)
- Configures AWS credentials from GitHub Secrets
- Downloads both pickle files from S3 into the runner workspace
- Builds Docker image (artifacts are included via `COPY . /app`)
- Pushes image to Amazon ECR

### Deployment — Continuous Deployment (self-hosted EC2 runner)
- Stops and removes the currently running container
- Prunes old Docker images to free disk space
- Pulls the latest image from ECR
- Runs the new container on port 8000 with AWS credentials injected as environment variables

**Key design decision:** Pickle files are excluded from Git (via `.gitignore`) and from the Docker build context (via `.dockerignore`) to avoid committing large binary files. They are pulled from S3 at build time and baked into the image — combining the benefits of clean version control with reproducible, self-contained deployments.

---

## 📂 Project Structure

```
movie_recommendation/
├── main.py                  # FastAPI app — endpoints, request/response models
├── utils.py                 # ML logic — artifact loading, similarity inference, TMDB fetch
├── statics/
│   └── home.html            # Frontend UI (vanilla JS, no framework)
├── artifacts/               # Gitignored — downloaded from S3 at build time
│   ├── movie_df.pkl
│   └── similarity_data.pkl
├── Dockerfile               # Python 3.12-slim image, uvicorn entrypoint
├── requirements.txt         # Project dependencies
├── .gitignore               # Excludes artifacts/, venv/, __pycache__
├── .dockerignore            # Excludes artifacts/ from build context (S3 supplies them)
└── .github/
    └── workflows/
        └── workflow.yml     # Full CI/CD pipeline
```

---

## ▶️ How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/your-username/movie_recommendation_system.git
cd movie_recommendation_system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download artifacts from S3**
```bash
mkdir -p artifacts
aws s3 cp s3://your-bucket/artifacts/ artifacts/ --recursive
```

**4. Run the app**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**5. Open in browser**
```
http://localhost:8000
```

---

## 💡 Key Engineering Highlights

**Precomputed similarity for O(1) inference** — The similarity matrix is computed once during model training and stored as a pickle. At request time, the lookup is a single indexed array access, not a computation — making the API fast regardless of dataset size.

**Artifact decoupling from source code** — Large binary model files are stored in S3, not Git. The CI/CD pipeline pulls them at build time, so the Git history stays clean and the Docker image stays reproducible.

**Absolute path resolution** — `utils.py` uses `os.path.abspath(__file__)` to resolve artifact paths relative to the module file itself, not the working directory. This ensures the app works correctly whether run locally, in Docker, or from any working directory.

**Structured error handling** — The `/recommend` endpoint catches `IndexError` (movie not found), `KeyError` (missing column), and generic exceptions separately, returning appropriate HTTP status codes and error messages to the client.

**Self-hosted EC2 runner** — The deployment job runs directly on the EC2 instance, eliminating the need for SSH steps or external deployment tools. The runner pulls the new image and restarts the container in place.

---

## 🔮 Future Improvements

- Add collaborative filtering to complement content-based recommendations
- Replace pickle with a vector database (e.g. FAISS, Pinecone) for scalable similarity search
- Cache TMDB poster responses in Redis to reduce external API calls
- Add a `/health` endpoint for load balancer health checks
- Implement model versioning to support rolling back to previous artifacts
- Add request logging and monitoring (e.g. AWS CloudWatch)

---

## 🔐 Environment & Secrets

The following secrets must be configured in GitHub repository settings:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | AWS region (e.g. `ap-south-1`) |
| `ECR_REPOSITORY_NAME` | ECR repository name |
| `AWS_ECR_LOGIN_URI` | ECR registry URI |
