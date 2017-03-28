from django.db import models
from datetime import date, datetime
from ..login.models import Userentry

class TaskManager(models.Manager):
    def add_task(self, data, session):
        errors = []
        try:
            entered_date = data['date']+data['time']
            entered_date_formatted = datetime.strptime(entered_date, '%Y-%m-%d%H:%M')
        except:
            errors.append("Please enter date and time")
            return(False, errors)
        print session['id']
        # entered_date = data['date']+data['time']
        print entered_date
        today = datetime.now()
        print today
        if len(data['task']) < 4:
            errors.append("Task Must Be 4 or more characters")
        if not data['date']:
            errors.append("Please enter a date")
        if not data['time']:
            errors.append("please enter a time")
        if datetime.strptime(entered_date, '%Y-%m-%d%H:%M') < today:
            errors.append("Please enter a future date")
        if errors:
            return(False, errors)
        else:
            user = Userentry.objects.get(id=session['id'])
            new_task = Task.objects.create(task=data['task'], date=data['date'], time=data['time'], status="Pending", owner=user )
            return(True, new_task)
    def edit_task(self, data, session):
        errors = []
        today = datetime.now()
        try:
            entered_date = data['date']+data['time']
            entered_date_formatted = datetime.strptime(entered_date, '%Y-%m-%d%H:%M')
        except:
            errors.append("Please enter date and time")
            return(False, errors)
        if len(data['task']) < 4:
            errors.append("Task Must Be 4 or more characters")
        if not data['date']:
            errors.append("Please enter a date")
        if not data['time']:
            errors.append("please enter a time")
        if datetime.strptime(entered_date, '%Y-%m-%d%H:%M') < today:
            errors.append("Please enter a future date")
        if errors:
            return(False, errors)
        else:
            user = Userentry.objects.get(id=session['id'])
            cur_task = Task.objects.get(id=session['task'])
            cur_task.task = data['task']
            cur_task.status = data['status']
            cur_task.date = data['date']
            cur_task.time = data['time']
            cur_task.save()
            return(True, cur_task)

class Task(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateField(auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    status = models.CharField(max_length=20)
    owner = models.ForeignKey(Userentry, related_name="task_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()
