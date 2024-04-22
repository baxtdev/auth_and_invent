from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, 'register.html')

def home(request):
    return render(request, 'index.html')
