from locust import HttpLocust, TaskSet
from corbel import iam


class UserBehavior(TaskSet):
    tasks = {}  # TODO


class WebsiteUser(HttpLocust):
    users = iam.generate_n_users(10)

    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

    iam.delete_users(users)
