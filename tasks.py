from locust import HttpLocust, TaskSet, task


def login(l):
    l.client.post("/login", {"username":"ellen_key", "password":"education"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class MyTaskSet(TaskSet):
    min_wait = 5000
    max_wait = 15000

    @task(3)
    def task1(self):
        index(self)
        print "task1"

    @task(6)
    def task2(self):
        profile(self)
        print "task2"

    def on_start(self):
        login(self)

class MyLocust(HttpLocust):
    task_set = MyTaskSet
