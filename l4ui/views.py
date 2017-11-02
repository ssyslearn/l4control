from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def create_l4(request):
    return render(request, 'l4ui/create_l4.html', {})
