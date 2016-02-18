from locust import HttpLocust, TaskSet, task
import sys
sys.path[0] = sys.path[0].rpartition('/test')[0]
from corbel import iam
from src.tracking import trackingSrc


# each locust will have their own user precreated in on_start
class UserBehavior(TaskSet):

    def on_start(self):
        print "user creation before doing any tasks"
        self.user = iam.create_user()

    @task
    def index(self):
        print "tracking.py:send_tracking"
        trackingSrc.send_tracking(self.user)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
