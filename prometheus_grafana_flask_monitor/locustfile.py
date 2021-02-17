from locust import HttpUser, TaskSet, task


class WebsiteUser(HttpUser):

    @task
    def index(self):
        self.client.get('/')

# locust -f locustfile.py -H http://localhost:5000