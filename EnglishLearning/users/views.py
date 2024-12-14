from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Count
from .serializer import UserSerializer


# ///////////////////////////////////////////////////////////////////////////
# ------------------------------- PROFILE -----------------------------------
# ///////////////////////////////////////////////////////////////////////////


# (Register:POST) a new user
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    data = request.data

    # Check for duplicate username or email
    if User.objects.filter(username=data.get("username")).exists():
        return Response(
            {"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST
        )
        # 400: Username already exists
    if User.objects.filter(email=data.get("email")).exists():
        return Response(
            {"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
        )
        # 400: Email already exists

    try:
        # Create the user
        User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )
        # 201: User successfully registered
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 500: Unexpected server error


# NOTE:(Retrieve:GET) user profile details
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile = request.user.profile
    user_data = {
        "username": profile.username,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "email": profile.email,
        "profile_img": request.build_absolute_uri(profile.profile_img.url),
    }
    return Response(user_data, status=status.HTTP_200_OK)
    # 200: Profile retrieved successfully




# get profile data:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_data(request):
    try:
        profile = request.user.profile
        data = {
            "username": profile.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email": profile.email,
            "profile_img": request.build_absolute_uri(profile.profile_img.url) if profile.profile_img else None,
            "profile_channel_art": request.build_absolute_uri(profile.profile_channel_art.url) if profile.profile_channel_art else None,
            "created_at": profile.created_at.strftime("%Y-%m-%d"),
        }
        return Response(data, status=status.HTTP_200_OK)
    except AttributeError as e:
        return Response({"error": "One or more profile fields are missing."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# update user:
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    username = request.data.get("username")
    email = request.data.get("email")
    
    # Check if the new username is taken
    if username and User.objects.filter(username=username).exclude(id=user.id).exists():
        return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the new email is taken
    if email and User.objects.filter(email=email).exclude(id=user.id).exists():
        return Response({"error": "Email already taken."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Update user fields
        user.username = username or user.username
        user.email = email or user.email
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.save()
        
        # print(request.data)    
        # Update profile fields with proper handling of file uploads
        profile = user.profile
        if "profile_image" in request.FILES:
            profile.profile_img = request.FILES["profile_image"]
        if "profile_channel_art" in request.FILES:
            profile.profile_channel_art = request.FILES["profile_channel_art"]
        profile.save()
        print(profile.profile_img)
        
        updated_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_img": request.build_absolute_uri(profile.profile_img.url) if profile.profile_img else None,
            "profile_channel_art": request.build_absolute_uri(profile.profile_channel_art.url) if profile.profile_channel_art else None,
        }
        
        return Response({"message": "Profile updated successfully.", "data": updated_data}, status=status.HTTP_200_OK)
    except ValueError as ve:
        return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred while updating the profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# delete profile:
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    try:    
        profile = request.user.profile
        profile.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get user decks count:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def decks_count(request):
    profile = request.user.profile
    data = {
        "decks_count": profile.decks.count(),
        "cards_count": profile.decks.aggregate(total_cards=Count('flashcards'))['total_cards'] or 0,
    }
    return Response(data, status=status.HTTP_200_OK)
