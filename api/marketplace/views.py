from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import TitleSerializer, AvatarSerializer
from .models import Title, Avatar


class TitleViewSet(viewsets.ModelViewSet):
    """
    Set of CRUD API endpoints for Titles.

    Note: All requests require the Custom API Key header
    Gamification-Api-Key: <key>

    ======================================
    POST TITLE
    ---------------------------------
    Description: Posts a new Title. Title.id and Title.name are unique values,
    Title.text is the actual Title users see. Cost is the price in shop_points

    Endpoint: http://localhost:8000/marketplace/titles/

    JSON structure:
    {
        "name": <title-name>,
        "text": <title-text>
        "cost": <int-value>
    }
    Optionally, other user fields can be added at entity creation.
    Including Title.partner for collaborators,
    Title.is_listed, which defaults to false and should be modified with different endpoints detailed below.
    Title.description for more details about the Title

    201 if successful, 400 Bad Request if Title name exists
    ---------------------------------
    ======================================

    GET TITLES
    ---------------------------------
    Description: Return the full list of Titles.
    Includes list of User.id's of those owning the title

    Endpoint: localhost:8000/marketplace/titles/
    JSON structure: No body required

    200 if successful
    ---------------------------------
    ======================================

    GET TITLE
    ---------------------------------
    Description: Return a single Title by their ID,

    Endpoint: http://localhost:8000/marketplace/titles/<id>/
    JSON structure: No body required

    404 Not Found if doesn't exist
    ---------------------------------
    ======================================

    DELETE TITLE
    ---------------------------------
    Description: Deletes Title from the database,
    Endpoint: http://localhost:8000/marketplace/titles/<id>/
    JSON structure: No body required

    204 No Content if successful, otherwise 404
    ---------------------------------
    ======================================

    PUT TITLE
    ---------------------------------

    Description: General update endpoint.
    Title.name is required but will be changed if different to the current name corresponding to the Title.id in the parameters

    Endpoint: localhost:8000/marketplace/titles/<id>/
    JSON structure:
    {
        "name": "name",
    }
    Plus any optional fields e.g. (text, cost, partner)

    Status 200 OK if successful, 400 Bad Request if missing required data
    """
    queryset = Title.objects.all().order_by('-date_time_added')
    serializer_class = TitleSerializer
    pagination_class = None

    @action(methods=['GET'], detail=False, url_path='name/(?P<name>[\\w\'\\!\\.\\,\\&\\?\\s]+)')
    def get_by_title(self, request, name):
        """
        GET BY TITLE NAME

        Definition: Endpoint to get Title by Title.name.
        Endpoint: http://localhost:8000/marketplace/titles/name/<name>/
        Request JSON structure: No body

        Returns 200 if found, 404 if Not Found.
        """
        title = get_object_or_404(Title, name=name)
        data = TitleSerializer(title, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='partner/(?P<partner>[\\w\'\\!\\.\\,\\&\\?\\s]+)')
    def get_by_partner(self, request, partner):
        """
        GET BY PARTNER NAME

        Definition: Endpoint to get Titles list for a given Collaborator.
        Endpoint: http://localhost:8000/marketplace/titles/partner/<partner>/
        Request JSON structure: No body

        Returns 200 if found, 404 if Not Found.
        """
        titles = Title.objects.filter(partner=partner).order_by('-partner')
        serializer = self.get_serializer(titles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], name="Listed Titles")
    def listed(self, request):
        """
        GET LISTED TITLES

        Definition: Endpoint to return all currently listed Titles.
        Endpoint: http://localhost:8000/marketplace/titles/listed/
        Request JSON structure: No body

        Returns 200 if found, empty Array if None.
        """
        titles = Title.objects.filter(is_listed=True).order_by('-date_time_listed')
        serializer = self.get_serializer(titles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], name="Unlisted Titles")
    def unlisted(self, request):
        """
        GET UNLISTED TITLES

        Definition: Endpoint to return all currently unlisted Titles.
        Endpoint: http://localhost:8000/marketplace/titles/unlisted/
        Request JSON structure: No body

        Returns 200 if found, empty Array if None.
        """
        titles = Title.objects.filter(is_listed=False).order_by('-date_time_listed')
        serializer = self.get_serializer(titles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], name="List/Unlist Title")
    def change_title_listing(self, request, *args, **kwargs):
        """
        LIST/UNLIST TITLE

        Description: Make Title purchaseable or unpurchaseable in the store
        Updates Title.is_listed bool, and Title.date_time_listed if listing
        or Title.date_time_unlisted if removing listing

        Endpoint: http://localhost:8000/marketplace/titles/<id>/change_title_listing/

        Request JSON structure:
        {
            "is_listed": <true/false>
        }

        200 OK if successful, 400 Bad Request if missing values, or if already in same listed state
        """
        title = self.get_object()
        print(request.data.get("is_listed"))
        # If missing values, return 400
        if request.data.get("is_listed") is None:
            data = {"message": "Missing is_listed value"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("is_listed") == title.is_listed:
            data = {"message": "Title.is_listed is already " + str(title.is_listed)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        is_listed_val = request.data.get("is_listed")

        # Update data based on bool
        if is_listed_val:
            data = {
                "is_listed": is_listed_val,
                "date_time_listed": datetime.now()}
        else:
            data = {
                "is_listed": is_listed_val,
                "date_time_unlisted": datetime.now()}

        # Update entity with updated data
        serializer = self.get_serializer(title, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AvatarViewSet(viewsets.ModelViewSet):
    """
    Set of CRUD API endpoints for Avatars.

    Note: All requests require the Custom API Key header
    Gamification-Api-Key: <key>

    ======================================
    POST Avatar
    ---------------------------------
    Description: Posts a new Avatar. Avatar.id and Avatar.name are unique values,
    Avatar.img_url is the uploaded img file. Cost is the price in shop_points

    Endpoint: http://localhost:8000/marketplace/avatars/

    JSON structure:
    {
        "name": <avatar-name>,
        "img_url": <url>
        "cost": <int-value>
    }
    Optionally, other user fields can be added at entity creation.
    Including Avatar.partner for collaborators,
    Avatar.is_listed, which defaults to false and should be modified with different endpoints detailed below.
    Avatar.description for more details about the Title

    201 if successful, 400 Bad Request if Avatar name exists
    ---------------------------------
    ======================================

    GET AVATARS
    ---------------------------------
    Description: Return the full list of Avatars.
    Includes list of User.id's of those owning the Avatar

    Endpoint: localhost:8000/marketplace/avatars/
    JSON structure: No body required

    200 if successful
    ---------------------------------
    ======================================

    GET AVATAR
    ---------------------------------
    Description: Return a single Avatar by their ID,

    Endpoint: http://localhost:8000/marketplace/avatars/<id>/
    JSON structure: No body required

    404 Not Found if doesn't exist
    ---------------------------------
    ======================================

    DELETE AVATAR
    ---------------------------------
    Description: Deletes Avatar from the database,
    Endpoint: http://localhost:8000/marketplace/avatars/<id>/
    JSON structure: No body required

    204 No Content if successful, otherwise 404
    ---------------------------------
    ======================================

    PUT AVATAR
    ---------------------------------

    Description: General update endpoint.
    Avatar.name is required but will be changed if different to the current name corresponding to the Avatar.id in the parameters

    Endpoint: localhost:8000/marketplace/avatars/<id>/
    JSON structure:
    {
        "name": "name",
    }
    Plus any optional fields e.g. (img_url, cost, partner)

    Status 200 OK if successful, 400 Bad Request if missing required data
    """
    queryset = Avatar.objects.all().order_by('-date_time_added')
    serializer_class = AvatarSerializer
    pagination_class = None

    @action(methods=['GET'], detail=False, url_path='name/(?P<name>[\\w\'\\!\\.\\,\\&\\?\\s]+)')
    def get_by_avatar(self, request, name):
        """
        GET BY AVATAR NAME

        Definition: Endpoint to get Avatar by Avatar.name.
        Endpoint: http://localhost:8000/marketplace/avatars/name/<name>/
        Request JSON structure: No body

        Returns 200 if found, 404 if Not Found.
        """
        avatar = get_object_or_404(Avatar, name=name)
        data = AvatarSerializer(avatar, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='partner/(?P<partner>[\\w\'\\!\\.\\,\\&\\?\\s]+)')
    def get_by_partner(self, request, partner):
        """
        GET BY PARTRNER NAME

        Definition: Endpoint to get Avatars list for a given Collaborator.
        Endpoint: http://localhost:8000/marketplace/avatars/partner/<partner>/
        Request JSON structure: No body

        Returns 200 if found, 404 if Not Found.
        """
        avatars = Avatar.objects.filter(partner=partner).order_by('-partner')
        serializer = self.get_serializer(avatars, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], name="Listed Avatars")
    def listed(self, request):
        """
        GET LISTED AVATARS

        Definition: Endpoint to return all currently listed Avatars.
        Endpoint: http://localhost:8000/marketplace/avatars/listed/
        Request JSON structure: No body

        Returns 200 if found, empty Array if None.
        """
        avatars = Avatar.objects.filter(is_listed=True).order_by('-date_time_listed')
        serializer = self.get_serializer(avatars, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], name="Unlisted Avatars")
    def unlisted(self, request):
        """
        GET UNLISTED AVATARS

        Definition: Endpoint to return all currently unlisted Avatars.
        Endpoint: http://localhost:8000/marketplace/avatars/unlisted/
        Request JSON structure: No body

        Returns 200 if found, empty Array if None.
        """
        avatars = Avatar.objects.filter(is_listed=False).order_by('-date_time_unlisted')
        serializer = self.get_serializer(avatars, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], name="List/Unlist Avatar")
    def change_avatar_listing(self, request, *args, **kwargs):
        """
        LIST/UNLIST AVATAR

        Description: Make Avatar purchaseable or unpurchaseable in the store
        Updates Avatar.is_listed bool, and Avatar.date_time_listed if listing
        or Avatar.date_time_unlisted if removing listing

        Endpoint: http://localhost:8000/marketplace/avatars/<id>/change_avatar_listing/

        Request JSON structure:
        {
            "is_listed": <true/false>
        }

        200 OK if successful, 400 Bad Request if missing values, or if already in same listed state
        """
        avatar = self.get_object()
        print(request.data.get("is_listed"))
        # If missing values, return 400
        if request.data.get("is_listed") is None:
            data = {"message": "Missing is_listed value"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("is_listed") == avatar.is_listed:
            data = {"message": "Avatar.is_listed is already " + str(avatar.is_listed)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        is_listed_val = request.data.get("is_listed")

        # Update data based on bool
        if is_listed_val:
            data = {
                "is_listed": is_listed_val,
                "date_time_listed": datetime.now()}
        else:
            data = {
                "is_listed": is_listed_val,
                "date_time_unlisted": datetime.now()}

        # Update entity with updated data
        serializer = self.get_serializer(avatar, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
