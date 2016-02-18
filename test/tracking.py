from locust import HttpLocust, TaskSet, task
import sys
sys.path[0] = sys.path[0].rpartition('/test')[0]
from corbel import iam
from src.tracking import tracking_src


# each locust will have their own user precreated in on_start
class UserBehavior(TaskSet):

    def on_start(self):
        self.user = iam.create_user()

    @task
    def index(self):
        tracking_src.send_tracking(self, self.user)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000
