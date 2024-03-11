from django.shortcuts import render

def academic_view(request):
    # Your view logic here
    return render(request, 'academic.html')

def jobs_view(request):
    # Your view logic here
    return render(request, 'jobs.html')
