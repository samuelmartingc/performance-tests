from locust import HttpLocust, TaskSet, task
from corbel import iam
# each locust will have their own user precreated in on_start
class UserBehavior(TaskSet):
    def on_start(self):
        print "user creation before doing any tasks"
        self.user = iam.generate_n_users(1)

    @task
    def index(self):
        print "locust instance id: %s" % self
        print "object user id %s" % self.user


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
