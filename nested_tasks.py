from locust import HttpLocust, TaskSet, task
class ForumPage(TaskSet):
    @task(20)
    def read_thread(self):
        print "forum: read_thread"
        pass

    @task(1)
    def new_thread(self):
        print "forum: new_thread"
        pass

    @task(5)
    def stop(self):
        print "forum: interrupted"
        #Third: is important to interrupt somewere this taskset
        #in order to go back to userbehaviour
        self.interrupt()

class UserBehaviour(TaskSet):
    #Second: one of the tasks is the taskset ForumPage with weight 5
    tasks = {ForumPage:5}

    @task
    def index(self):
        print "userBehaviour default"
        pass

class MyLocust(HttpLocust):
    #First: invocation of taskset UserBehaviour
    task_set = UserBehaviour
