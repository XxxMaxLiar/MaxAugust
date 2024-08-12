from django.db import models
import datetime
import django

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
    now_time = django.utils.timezone.localtime()
    no_leave_visits = Visit.objects.filter(leaved_at=None)
    
    for no_leave_visit in no_leave_visits:
        who_entered = no_leave_visit.passcard.owner_name
        entered_at = no_leave_visit.entered_at
        duration = now_time - entered_at
        return who_entered, entered_at, duration
    

def format_duration():
    who_entered, entered_at, duration = get_duration()
    return {'who_entered': who_entered, 'entered_at': entered_at, 'duration': duration}


def is_visit_long(n):
    now_time = django.utils.timezone.localtime()
    passcard = Passcard.objects.all[n]
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        entered_time = visit.entered_at
        leaved_time = visit.leaved_at

        if leaved_time == None: #проверка, что человек находится в хранилище
            duration = now_time - entered_time
            return entered_time, duration, 'Человек находится в хранилище'
        
        delta = leaved_time-entered_time
        if delta/60 > 60:       #проверка, что человек находится дольша часа в хранилище
            is_strange = True   #это странно - True
            return entered_time, delta, is_strange
        
        if delta/60 <= 60:      #проверка, что человек находится не больше часа в хранилище
            is_strange = False  #это странно - False
            return entered_time, delta, is_strange
        