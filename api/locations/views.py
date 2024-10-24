from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CheckInLocation
from .serializers import CheckInLocationSerializer
from user.models import CustomUser

class CheckInLocationViewSet(viewsets.ModelViewSet):
    queryset = CheckInLocation.objects.all()
    serializer_class = CheckInLocationSerializer

    @action(detail=False, methods=['POST'], name="Add Check-In Location")
    def add_checkin(self, request):
        """
        Adds a new check-in for a user at an event location.
        """
        user_id = request.data.get('user_id')
        event_name = request.data.get('event_name')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Check for missing fields
        if not user_id or not event_name or not latitude or not longitude:
            return Response({"message": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure user exists
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure user has not already checked into this event
        if CheckInLocation.objects.filter(user=user, event_name=event_name).exists():
            return Response({"message": "User has already checked in to this event."}, status=status.HTTP_400_BAD_REQUEST)

        # Create new check-in
        checkin = CheckInLocation.objects.create(
            user=user,
            event_name=event_name,
            latitude=latitude,
            longitude=longitude
        )

        # Return newly created check-in
        return Response(CheckInLocationSerializer(checkin).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], name="Get User Check-Ins")
    def user_checkins(self, request, pk=None):
        """
        Retrieves all check-ins for a specific user.
        """
        # Ensure user exists
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all check-ins for this user
        checkins = CheckInLocation.objects.filter(user=user)
        serializer = CheckInLocationSerializer(checkins, many=True)
        
        # Return all check-ins for this user
        return Response(serializer.data, status=status.HTTP_200_OK)
