from django.shortcuts import render

# Create your views here.

def create_l4(request):
    return render(request, 'l4ui/create_l4.html', {})
