from django.shortcuts import render

def blog1_view(request):
    # Your view logic here
    return render(request, 'blog1.html')

def blog2_view(request):
    # Your view logic here
    return render(request, 'blog2.html')
