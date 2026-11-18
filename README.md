# Social Club Lab — GTA6 Launch Day Chaos

> **Note:** This app is a deliberately fragile, fictional training replica. The `.env` credentials are fake. Do not deploy this outside a local lab environment.

---

## Background

GTA VI just dropped. 40 million players hit the login server simultaneously. It fell over.

You're the ops team. You have two problems to fix, then the server is yours to improve.

---

## Getting Started

```bash
docker compose up --build
```

Visit: `http://localhost:8080`

The app should load — a Rockstar Social Club styled login page. Try submitting the form. It works, but just barely.

---

## Challenge 1: Load Resilience

### The problem

Run the load test to simulate launch day traffic:

```bash
# Install locust if you don't have it
pip install locust

# Run the test
locust -f locustfile.py --host http://localhost:8080 --users 200 --spawn-rate 20 --headless --run-time 60s
```

Watch what happens. The single Flask container struggles to keep up.

### Your task

Introduce load balancing so the app stays responsive under load.

**Expected approach:**
1. Scale Flask to multiple replicas in `docker-compose.yml`
2. Add an **Nginx** reverse proxy to distribute requests across them
3. Complete the starter config in `nginx/nginx.conf`
4. Re-run the load test and confirm the app holds up

**Success criteria:**
- `docker compose ps` shows multiple Flask replicas
- `http://localhost:8080/health` returns `200` consistently under load
- The load test shows no (or minimal) failures

**Useful commands:**
```bash
# Scale replicas
docker compose up --scale flask=3 --build

# Watch container stats
docker stats

# Check which replica handled a request
docker compose logs flask
```

---

## Challenge 2: Accidental `.env` in Docker Image

### The problem

A `.env` file was accidentally committed to the repo. The `Dockerfile` uses `COPY . .` — which means the `.env` and its contents are baked into every image layer.

**Verify it yourself:**
```bash
docker build -t social-club-lab .
docker run --rm social-club-lab cat /app/.env
```

You should see the credentials. Even if you add `RUN rm /app/.env` to the Dockerfile, the secrets remain in the earlier layer — anyone with access to the image can retrieve them.

### Your task

Fix the Dockerfile so the `.env` is never included in the image.

**Two valid approaches:**

**Option A — `.dockerignore`:**
Create a `.dockerignore` file in the repo root that excludes `.env` from the build context.

**Option B — Multi-stage build:**
Restructure the Dockerfile to use a multi-stage build so secrets never enter the final image.

**Verify your fix:**
```bash
docker build -t social-club-lab .
docker run --rm social-club-lab cat /app/.env
# Should return: cat: /app/.env: No such file or directory
```

**Key concept to understand:**
Docker images are built in layers. A file copied in an early layer and deleted in a later layer is still present in the image history — `docker history` and layer inspection tools can retrieve it. The only safe fix is to never copy the file into the build context in the first place.

---

## Open-Ended Improvements

Both challenges done? The server is yours. Some ideas:

- **Rate limiting** — add `flask-limiter` to throttle requests per IP
- **Redis session caching** — reduce load on Flask with a caching layer
- **HTTPS** — configure Nginx with a self-signed cert
- **Secret management** — replace `.env` with Docker secrets or runtime environment injection
- **Monitoring** — add Prometheus + Grafana to visualise request throughput
- **Real login flow** — wire up a SQLite database and proper session handling
- **UI improvements** — improve the login page design

---

## Tips

```bash
# Rebuild after changes
docker compose up --build

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Inspect image layers
docker history social-club-lab

# Open a shell inside a running container
docker compose exec flask bash
```

---

## Cleanup

```bash
docker compose down --rmi all --volumes
```
