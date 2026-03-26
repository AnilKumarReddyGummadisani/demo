# Python CRUD Demo

A production-ready **CRUD REST API** built with **FastAPI**, containerised with **Docker**, deployed to **Kubernetes** via **GitHub Actions** CI/CD — structured like a Java Maven project.

## Project Structure (Java Maven analogy)

```
demo/
├── app/                          # src/main/java
│   ├── main.py                   # Application entry point (Spring Boot main class)
│   ├── models/
│   │   └── item.py               # DTOs / POJOs
│   ├── repository/
│   │   └── item_repository.py    # DAO / Repository layer
│   └── routes/
│       └── items.py              # Controller / REST endpoints
├── tests/                        # src/test/java
│   └── test_items.py             # JUnit-equivalent tests
├── requirements.txt              # pom.xml dependencies
├── requirements-dev.txt          # test-scoped dependencies
├── pyproject.toml                # pom.xml (project metadata)
├── Dockerfile                    # Multi-stage build
├── .dockerignore
├── k8s/                          # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── .github/workflows/
    └── ci-cd.yaml                # GitHub Actions pipeline
```

## API Endpoints

| Method | URL                   | Description     |
|--------|-----------------------|-----------------|
| GET    | `/health`             | Health check    |
| POST   | `/api/v1/items/`      | Create an item  |
| GET    | `/api/v1/items/`      | List all items  |
| GET    | `/api/v1/items/{id}`  | Get item by ID  |
| PUT    | `/api/v1/items/{id}`  | Update an item  |
| DELETE | `/api/v1/items/{id}`  | Delete an item  |

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload

# Open API docs → http://localhost:8000/docs
```

## Run Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Docker

```bash
# Build
docker build -t python-crud-demo .

# Run
docker run -p 8000:8000 python-crud-demo
```

## CI/CD Pipeline (GitHub Actions)

The pipeline has **3 stages** (analogous to a Java Maven CI/CD):

| Stage              | Maven Analog          | What it does                                         |
|--------------------|-----------------------|------------------------------------------------------|
| **Test**           | `mvn test`            | Installs deps, runs pytest with coverage ≥ 80%       |
| **Build & Push**   | `mvn package` + push  | Multi-stage Docker build → push to Docker Hub        |
| **Deploy**         | K8s deploy            | `kubectl apply` deployment + service to cluster      |

### Required GitHub Secrets

| Secret            | Description                              |
|-------------------|------------------------------------------|
| `DOCKER_USERNAME` | Docker Hub username                      |
| `DOCKER_PASSWORD` | Docker Hub access token                  |
| `KUBECONFIG`      | Base64-encoded kubeconfig for the cluster|

## Kubernetes

```bash
# Manual deploy
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods -n crud-demo
kubectl get svc  -n crud-demo
```

The app is exposed via a `LoadBalancer` service on port **80** → forwarded to container port **8000**.
