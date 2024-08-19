from django.db import models
import datetime
import django
from django.http import Http404
from django.shortcuts import get_object_or_404
class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )







def get_duration():
    a = []
    now_time = django.utils.timezone.localtime()
    no_leave_visits = Visit.objects.filter(leaved_at=None)
    
    for no_leave_visit in no_leave_visits:
        who_entered = no_leave_visit.passcard.owner_name
        entered_at = no_leave_visit.entered_at
        duration = now_time - entered_at
        b = {'who_entered': who_entered, 'entered_at': entered_at, 'duration': duration}
        a.append(b)
    return a

passcode = '5a746f24-2a46-4d4e-a076-d56689c8dcb7' #здесь вводим id человека, которого хотим найти
def is_visit_long():
    a = []
    now_time = django.utils.timezone.localtime()
    crud_post = Passcard.objects.get(passcode = passcode)
    visits = Visit.objects.filter(passcard = crud_post)
    for visit in visits:
        entered_time = visit.entered_at
        leaved_time = visit.leaved_at
        if leaved_time == None: #проверка, что человек находится в хранилище
            delta = now_time - entered_time
            is_strange = True
            b = {'entered_at': entered_time, 'duration': delta, 'is_strange': is_strange}
            a.append(b)
            continue
        delta = leaved_time - entered_time
        if delta.seconds/60 > 60:       #проверка, что человек находится дольша часа в хранилище
            is_strange = True   #это странно - True
            b = {'entered_at': entered_time, 'duration': delta, 'is_strange': is_strange}
            a.append(b)
            continue
        if delta.seconds/60 <= 60:      #проверка, что человек находится не больше часа в хранилище
            delta = leaved_time-entered_time
            is_strange = False  #это странно - False
            b = {'entered_at': entered_time, 'duration': delta, 'is_strange': is_strange}
            a.append(b)
    return a
