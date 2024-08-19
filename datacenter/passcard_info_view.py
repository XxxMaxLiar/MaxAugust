from datacenter.models import Passcard
from datacenter.models import Visit, is_visit_long
from datacenter.models import passcode
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def passcard_info_view(request, passcode):
    passcard = Passcard.objects.all()
    crud_post = get_object_or_404(Passcard, passcode = passcode)
    # Программируем здесь
    
    
    this_passcard_visits = is_visit_long()
    
    context = {
        'passcard': crud_post,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)