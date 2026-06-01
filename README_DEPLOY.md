Deployment Guide — AeroSpy
=========================

This guide shows how to containerize and deploy the Streamlit app.

1) Quick local Docker run

```bash
# build image
docker build -t aerospy:latest .

# run container locally (port 8501)
docker run --rm -p 8501:8501 --name aerospy aerospy:latest
```

Open http://localhost:8501

2) Using docker-compose (dev)

```bash
docker-compose up --build -d
docker-compose logs -f
```

3) Push to Docker Hub (for cloud deployment)

```bash
docker tag aerospy:latest <your-dockerhub-username>/aerospy:latest
docker push <your-dockerhub-username>/aerospy:latest
```

4) Run on a cloud VM (recommended for production)

- Create a VM (AWS EC2 / GCP Compute Engine / Azure VM). For inference speed consider a GPU instance.
- Install Docker on the VM.
- Pull and run the image on the VM:

```bash
docker run -d --restart unless-stopped -p 80:8501 \
  -v /path/to/model:/app  \
  --name aerospy <your-dockerhub-username>/aerospy:latest
```

Notes for GPU
- If you need GPU acceleration, build a GPU-ready image using an NVIDIA CUDA base image and install the appropriate `torch`/`torchvision` wheels for your CUDA version. On a GPU host install NVIDIA Container Toolkit and run containers with `--gpus all`.

Streamlit Cloud
- Streamlit Community Cloud can run this repo directly (via GitHub) but has limitations (no GPU, disk and runtime limits). If you have light workloads it is the fastest way to publish.

CI/CD
- Add GitHub Actions to build and push the Docker image on push to `main`.
