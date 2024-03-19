# from django.urls import path
# from .views import events_view, delete_event

# app_name = "events"

# urlpatterns = [
#     path('events/', events_view, name='events'),
#     path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
# ]



from django.urls import path
from .views import events_view, delete_event, participate_event, create_event_view

app_name = "events"

urlpatterns = [
    path('events/', events_view, name='events'),
    path('create_event/', create_event_view, name='create_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
    path('events/participate/<int:event_id>/', participate_event, name='participate_event'),
]
