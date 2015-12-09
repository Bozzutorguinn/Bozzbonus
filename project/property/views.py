from django.shortcuts import render

def PropertyIndex(request):
    return render(request, 'property/index.html')
