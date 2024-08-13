from django.urls import path
from .views import add_event, remove_event, get_events, remove_recurrence_event

urlpatterns = [
    path('add/', add_event, name='add_event'),
    path('events/<int:year>/<int:month>/<int:day>/', get_events, name='get_events'),
    path('remove/<uuid:id>/<int:year>/<int:month>/<int:day>/', remove_recurrence_event, name='remove_recurrence_event'),
    path('remove/<uuid:id>/', remove_event, name='remove_event'),
]