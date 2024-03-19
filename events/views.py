# from django.shortcuts import render
# from .forms import CollegeEventCreationForm
# from django.contrib.auth.decorators import login_required

# @login_required
# def events_view(request):
#     print("events_view function called")
#     if request.method == 'POST':
#         print("Request method is POST")
#         form = CollegeEventCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             print("Form is valid")
#             event = form.save(commit=False)
#             event.organizer = request.user.userprofile
#             event.created_by = request.user
#             event.save()
#             form.save_m2m()
#             print("Event saved successfully")
#             # Instead of redirecting, render the events.html template
#             return render(request, 'events.html', {'form': CollegeEventCreationForm()})
#         else:
#             print("Form is invalid")
#             print(form.errors)
#     else:
#         print("Request method is not POST")
#         form = CollegeEventCreationForm()    
#     return render(request, 'events.html', {'form': form})


# @login_required
# def events_view(request):
#     print("events_view function called")
#     form = CollegeEventCreationForm()  # Create an instance of the form
#     events = CollegeEvent.objects.all()  # Fetch all events
#     if request.method == 'POST':
#         print("Request method is POST")
#         form = CollegeEventCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             print("Form is valid")
#             event = form.save(commit=False)
#             event.organizer = request.user.userprofile
#             event.created_by = request.user
#             event.save()
#             form.save_m2m()
#             print("Event saved successfully")
#             # After saving the event, fetch all events again
#             events = CollegeEvent.objects.all()
#         else:
#             print("Form is invalid")
#             print(form.errors)

#     return render(request, 'events.html', {'form': form, 'events': events})





from django.shortcuts import render
from .forms import CollegeEventCreationForm
from .models import CollegeEvent
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .forms import CollegeEventCreationForm
from .models import CollegeEvent
from django.contrib.auth.decorators import login_required

@login_required
def events_view(request):
    print("events_view function called")
    form = CollegeEventCreationForm()  # Create an instance of the form
    events = CollegeEvent.objects.all()  # Fetch all events
    created_events = CollegeEvent.objects.filter(created_by=request.user)  # Fetch events created by the current user
    
    # Fetch events where the user is a participant
    participated_events = CollegeEvent.objects.filter(participants=request.user)

    if request.method == 'POST':
        print("Request method is POST")
        form = CollegeEventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            event = form.save(commit=False)
            event.organizer = request.user.userprofile
            event.created_by = request.user
            event.save()
            form.save_m2m()
            print("Event saved successfully")
            # After saving the event, fetch all events again
            events = CollegeEvent.objects.all()
            created_events = CollegeEvent.objects.filter(created_by=request.user)  # Update created events after saving new event
        else:
            print("Form is invalid")
            print(form.errors)

    return render(request, 'events.html', {'form': form, 'events': events, 'created_events': created_events, 'participated_events': participated_events})





from django.shortcuts import get_object_or_404, redirect
from .models import CollegeEvent

@login_required
def delete_event(request, event_id):
    print("delete_event function called")
    event = get_object_or_404(CollegeEvent, pk=event_id)
    event.delete()
    print("Event deleted successfully")
    
    return redirect('events:events')


from django.shortcuts import get_object_or_404, redirect
from .models import CollegeEvent
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def participate_event(request, event_id):
    print("participate_event function called")
    event = get_object_or_404(CollegeEvent, pk=event_id)
    
    # Logic to handle participation status
    if request.user in event.participants.all():
        # User is already participating, so remove participation
        event.participants.remove(request.user)
        print("User removed participation from event with ID:", event_id)
    else:
        # User is not participating, so add participation
        event.participants.add(request.user)
        print("User participated in event with ID:", event_id)
    
    # Redirect back to the events page
    return HttpResponseRedirect(reverse('events:events'))

def create_event_view(request):
    # Your view logic here
    return render(request, 'create_event.html')
