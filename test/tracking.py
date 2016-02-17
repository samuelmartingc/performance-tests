from locust import HttpLocust, TaskSet, task
from corbel import iam
from src.tracking import tracking


# each locust will have their own user precreated in on_start
class UserBehavior(TaskSet):

    def on_start(self):
        print "user creation before doing any tasks"
        self.user = iam.create_user()

    @task
    def index(self):
        print "helloasf"
        tracking.send_tracking(self.user)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
