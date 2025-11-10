from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Disable SSL certificate verification for all requests
        self.client.verify = False

    @task(3)
    def list_authors(self):
        """Fetch all authors"""
        self.client.get("/api/v1/authors/")

    @task(2)
    def list_books(self):
        """Fetch all books"""
        self.client.get("/api/v1/books/")

    @task(1)
    def list_borrowers(self):
        """Fetch all borrowers"""
        self.client.get("/api/v1/borrowers/")
