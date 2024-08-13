import math

from rest_framework import status
import logging
from ..models import Event, EventException
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer

logger = logging.getLogger('events')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_event(request):
    logger.info('Attempting to add a new event for user: %s', request.user)
    serializer = EventSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        event = serializer.save()
        logger.info('Event created: %s', serializer.data)
        return JsonResponse({'id': event.id})
    else:
        logger.warning('Event creation failed: %s', serializer.errors)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_recurrence_event(request, id, year, month, day):
    logger.info('Attempting to remove a recurrence event with ID: %s on %s-%s-%s for user: %s', id, year, month, day, request.user)
    start_of_day = int(datetime(year, month, day).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    end_of_day = start_of_day + 86399
    event = get_object_or_404(Event, id=id, user=request.user, start_at__lt=end_of_day)
    logger.debug('Candidate event: %s', event)


    if event.period:
        delta_seconds = math.fabs(start_of_day - event.start_at)
        delta_days = math.ceil(delta_seconds / 86400)

        if delta_days % event.period == 0 or start_of_day <= event.start_at <= end_of_day:
            EventException.objects.get_or_create(event=event, exception_date=start_of_day)
            return JsonResponse(data={'status': 'deleted', 'date': datetime(year, month, day), 'id': id},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"error": "This date does not match the event's recurrence pattern."},
                                status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "This event does not have a recurrence pattern."},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_event(request, id):
    logger.info('Attempting to remove event with ID: %s for user: %s', id, request.user)
    event = get_object_or_404(Event, id=id, user=request.user)
    event.delete()
    return JsonResponse(data={'status': 'deleted', 'id': id}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request, year, month, day):
    logger.info('Fetching events for user: %s on %s-%s-%s', request.user, year, month, day)

    start_of_day = int(datetime(year, month, day).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    end_of_day = start_of_day + 86399

    events = Event.objects.filter(start_at__lt=end_of_day, user=request.user)
    result_events = []

    for event in events:
        if event.period:
            delta_seconds = math.fabs(start_of_day - event.start_at)
            delta_days = math.ceil(delta_seconds / 86400)

            if delta_days % event.period == 0 or start_of_day <= event.start_at <= end_of_day:
                if not event.exceptions.filter(exception_date=start_of_day).exists():
                    result_events.append(event)
        else:
            event_date = datetime.utcfromtimestamp(event.start_at).date()
            if event_date == datetime(year, month, day).date():
                result_events.append(event)

    serializer = EventSerializer(result_events, many=True)
    return JsonResponse(serializer.data, safe=False)
