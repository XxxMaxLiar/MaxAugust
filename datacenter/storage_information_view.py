from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь

    non_closed_visits = get_duration()
    
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
