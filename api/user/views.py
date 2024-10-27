
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from marketplace.models import Avatar, Title
from marketplace.serializers import AvatarSerializer, TitleSerializer
from .serializers import CustomUserSerializer
from .models import CustomUser
from user.models import update_user_points


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Set of CRUD API endpoints for the User entity.

    Note: All requests require the Custom API Key header
    Gamification-Api-Key: <key>

    ======================================
    POST USER
    ---------------------------------
    Description: Posts a new user,
    Endpoint: http://localhost:8000/users/users/

    JSON structure:
    {
        "username": "username",
        "titles": [],
        "avatars": []
    }
    Optionally, other user fields can be added at entity creation, e.g. experience_points, shop_points.

    201 if successful, 400 Bad Request if username exists
    ---------------------------------
    ======================================

    GET USERS
    ---------------------------------
    Description: Return the full list of users and their owned items
    Endpoint: localhost:8000/users/users/
    JSON structure: No body required

    200 if successful
    ---------------------------------
    ======================================

    GET USER
    ---------------------------------
    Description: Return a single user by their ID,
    Endpoint: http://localhost:8000/users/users/<id>/
    JSON structure: No body required

    404 Not Found if doesn't exist
    ---------------------------------
    ======================================

    DELETE USER
    ---------------------------------
    Description: Deletes user from the database,
    Endpoint: http://localhost:8000/users/users/<id>/
    JSON structure: No body required

    204 No Content if successful, otherwise 404
    ---------------------------------
    ======================================

    PUT USER
    ---------------------------------

    Description: Updates user fields. Username is required.
    Endpoint: localhost:8000/users/users/<id>/
    JSON structure:
    {
        "username": "username",
        "titles": [],
        "avatars": [],
    }
    Plus any optional fields.

    Status 200 OK if successful, 400 Bad Request if missing data
    """
    queryset = CustomUser.objects.all().order_by('-username')
    serializer_class = CustomUserSerializer
    pagination_class = None

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """
        LEADERBOARD
        """
        users = CustomUser.objects.filter(is_admin=False).order_by('-points_accumulated')[:10]  # get top 10 user and without superusers
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], name="Add points")
    def add_points(self, request, *args, **kwargs):
        """
        PATCH USER POINTS

        Description: Add experience_points and shop_points to user entity.
        Int values must be >= 0

        Endpoint: http://localhost:8000/users/users/<id>/add_points/

        Request JSON structure:
        {
            "experience_points": <int_value>,
            "shop_points": <int_value>
        }

        200 OK if successful, 400 Bad Request if missing values
        """
        user = self.get_object()

        # If missing values, return 400
        if not request.data.get("experience_points") or not request.data.get("shop_points"):
            data = {"message": "Missing points values"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # If attempting to deduct points
        if request.data.get("experience_points") < 0 or request.data.get("shop_points") < 0:
            data = {"message": "Can not add negative points"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # Points values to add
        new_experience_points = int(request.data.get("experience_points"))
        new_shop_points = int(request.data.get("shop_points"))

        # Create points log for data, and save points to user
        update_user_points(user, new_experience_points, new_shop_points)

        # Choose updated data to serialize
        data = {"experience_points": user.experience_points, "shop_points": user.shop_points}

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer) - done by update_user_points

        return Response(serializer.data)

    @action(detail=True, methods=['PUT'], name="Update Current Title")
    def current_title(self, request, *args, **kwargs):
        """
        UPDATE CURRENT TITLE

        Description: Choose one Title owned by the user to be their current title
        for profile display purposes

        Endpoint: http://localhost:8000/users/users/<id>/current_title/

        Request JSON structure:
        {
            "title_id": <int_value>
        }

        200 OK if successful, 400 Bad Request if missing values
        """
        # Get User from ID parameter in URL
        user = self.get_object()
        # Get Title matching request ID
        title = get_object_or_404(Title.objects.filter(id=request.data.get("title_id")))
        
        # Check for Title ownership
        if (not user.titles.filter(id=title.id)):
            data = {"message": "User does not own this Title."}
            return Response(data, status=status.HTTP_200_OK)

        # Data to update
        data = {
            "current_title": {
                "id": title.id
            }
        }

        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['PUT'], name="Update Current Avatar")
    def current_avatar(self, request, *args, **kwargs):
        """
        UPDATE CURRENT AVATAR

        Description: Choose one Avatar owned by the user to be their current title
        for profile display purposes

        Endpoint: http://localhost:8000/users/users/<id>/current_avatar/

        Request JSON structure:
        {
            "avatar_id": <int_value>
        }

        200 OK if successful, 400 Bad Request if missing values
        """
        # Get User from ID parameter in URL
        user = self.get_object()
        # Get Title matching request ID
        avatar = get_object_or_404(Avatar.objects.filter(id=request.data.get("avatar_id")))
        
        # Check for Avatar ownership
        if (not user.avatars.filter(id=avatar.id)):
            data = {"message": "User does not own this Avatar."}
            return Response(data, status=status.HTTP_200_OK)

        # Data to update
        data = {
            "current_avatar": {
                "id": avatar.id
            }
        }

        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['PUT'], name="Buy Avatar")
    def buy_avatar(self, request, *args, **kwargs):
        """
        BUY AVATAR

        Definition: Given an Avatar ID,
        if the current user specified by their ID in the URL parameters has enough shop_points,
        and does not own the Avatar already,
        Add the Avatar to the user's list of Avatars,
        and deduct the cost amount from their shop_points.

        Endpoint: http://localhost:8000/users/users/5/buy_avatar/

        Request JSON structure:
        {
            "avatar_id: <id>
        }

        Returns 404 if UID, or Avatar ID don't exist.
        """
        # Get user from id parameter in URL
        user = self.get_object()
        # Get avatar matching
        avatar = get_object_or_404(Avatar.objects.filter(id=request.data.get("avatar_id")))

        # Check if already owned
        if (user.avatars.filter(id=avatar.id)):
            data = {"message": "User already owns this item."}
            return Response(data, status=status.HTTP_200_OK)

        # Check for available funds
        if (avatar.cost > user.shop_points):
            data = {"message": "User does not have enough points to buy this item"}
            return Response(data, status=status.HTTP_200_OK)
        
        # Check if Avatar is for sale
        if (not avatar.is_listed):
            data = {"message": "Avatar is not available for purchase"}
            return Response(data, status=status.HTTP_200_OK)

        # Deduct shop_points and add to user Avatars, M2M Manager handles the update
        new_shop_points = user.shop_points - avatar.cost
        user.avatars.add(avatar.id)         
        
        # Data to update, 
        # Nested writable ManyToMany relationship is handled by the ManyRelatedManager and does not need to be added in the data
        data = {
            "shop_points": new_shop_points,
        }
        
        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name="Refund Avatar")
    def refund_avatar(self, request, *args, **kwargs):
        """
        REFUND AVATAR

        Definition: Given a Avatar ID,
        if the current user specified by their ID in the URL parameters has the requested refund Avatar,
        Remove the Avatar to the user's list of Avatars,
        and add the cost amount to their shop_points.

        Endpoint: http://localhost:8000/users/users/<user_id>/refund_avatar/

        Request JSON structure:
        {
            "avatar_id: <id>
        }

        Returns 404 if User ID, or Avatar ID don't exist.
        """
        # Get User from ID parameter in URL
        user = self.get_object()
        # Get Avatar matching request ID
        avatar = get_object_or_404(Avatar.objects.filter(id=request.data.get("avatar_id")))
        
        # Get initial Avatar in case of removing all other Avatar objects from the User
        base_avatar = get_object_or_404(Avatar.objects.filter(id=1))

        # Check if not already owned
        if (not user.avatars.filter(id=avatar.id)):
            data = {"message": "User does not own this item."}
            return Response(data, status=status.HTTP_200_OK)
        
        # Check if trying to refund base Avatar
        if (avatar.id == base_avatar.id):
            data = {"message": "Can not refund base Avatar."}
            return Response(data, status=status.HTTP_200_OK)
        
        # Deduct shop_points
        new_shop_points = user.shop_points + avatar.cost
        
        # Data to update
        # If Avatar being refunded is current Avatar, current Avatar is base Avatar  
        data = {
            "shop_points": new_shop_points,
        }
        
        # Remove Avatar from User M2M list
        user.avatars.remove(avatar.id)

        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['PUT'], name="Buy Title")
    def buy_title(self, request, *args, **kwargs):
        """
        BUY TITLE

        Definition: Given a Title ID,
        if the current user specified by their ID in the URL parameters has enough shop_points,
        and does not own the Title already,
        Add the Title to the user's list of Titles,
        and deduct the cost amount from their shop_points.

        Endpoint: http://localhost:8000/users/users/<user_id>/buy_title/

        Request JSON structure:
        {
            "title_id: <id>
        }

        Returns 404 if User ID, or Title ID don't exist.
        """
        # Get User from ID parameter in URL
        user = self.get_object()
        # Get Title matching request ID
        title = get_object_or_404(Title.objects.filter(id=request.data.get("title_id")))

        # Check if already owned
        if (user.titles.filter(id=title.id)):
            data = {"message": "User already owns this item."}
            return Response(data, status=status.HTTP_200_OK)

        # Check for available funds
        if (title.cost > user.shop_points):
            data = {"message": "User does not have enough points to buy this item"}
            return Response(data, status=status.HTTP_200_OK)
        
        # Check if title is for sale
        if (not title.is_listed):
            data = {"message": "Title is not available for purchase"}
            return Response(data, status=status.HTTP_200_OK)

        # Deduct shop_points and add to user Titles
        new_shop_points = user.shop_points - title.cost
        user.titles.add(title.id)

        # Data to update,
        # Nested writable ManyToMany relationship is handled by the ManyRelatedManager and does not need to be added in the data
        data = {
            "shop_points": new_shop_points,
        }

        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name="Refund Title")
    def refund_title(self, request, *args, **kwargs):
        """
        REFUND TITLE

        Definition: Given a Title ID,
        if the current user specified by their ID in the URL parameters has the requested refund Title,
        Remove the Title to the user's list of Titles,
        and add the cost amount to their shop_points.

        Endpoint: http://localhost:8000/users/users/<user_id>/refund_title/

        Request JSON structure:
        {
            "title_id: <id>
        }

        Returns 404 if User ID, or Title ID don't exist.
        """
        # Get User from ID parameter in URL
        user = self.get_object()
        # Get Title matching request ID
        title = get_object_or_404(Title.objects.filter(id=request.data.get("title_id")))
        # Get initial Title in case of removing all other Title objects from the User
        base_title = get_object_or_404(Title.objects.filter(id=1))

        # Check if not already owned
        if (not user.titles.filter(id=title.id)):
            data = {"message": "User does not own this item."}
            return Response(data, status=status.HTTP_200_OK)
        
        # Check if trying to refund base Title
        if (title.id == base_title.id):
            data = {"message": "Can not refund base Title."}
            return Response(data, status=status.HTTP_200_OK)
        
        # Deduct shop_points
        new_shop_points = user.shop_points + title.cost
        
        # Data to update     
        data = {
            "shop_points": new_shop_points,
        }
        
        # Remove Avatar from User M2M list
        user.titles.remove(title.id)

        # Parse data and update the User model
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='username/(?P<username>[\\w\\s]+)')
    def get_by_username(self, request, username):
        """
        GET BY USERNAME

        Definition: Endpoint to get user by username.

        Endpoint: http://localhost:8000/users/users/username/<username>/

        Request JSON structure: No body

        Returns 200 if found, 404 if Not Found.
        """
        user = get_object_or_404(CustomUser, username=username)
        data = CustomUserSerializer(user, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
