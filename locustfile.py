from locust import HttpUser, task, between


class SocialClubUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(2)
    def homepage(self):
        self.client.get("/")

    @task(3)
    def login(self):
        self.client.post(
            "/login",
            json={"username": "player123", "password": "password"},
            name="/login",
        )

    @task(1)
    def health(self):
        self.client.get("/health")
