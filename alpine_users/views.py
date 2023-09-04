from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer
from .models import User


@api_view(["POST"])
def obtain_token(request):
    # get username and login fields from the request.data
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        # check if user exists
        user = User.objects.get(username=username)

        # if user exists get token
        if user.check_password(password):
            # get user data using the custom serializer
            serializer = UserSerializer(user)

            #  get refresh token
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
    except User.DoesNotExist:
        pass

    return Response(
        {"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(["GET"])
def get_user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def register_user(request):
    # get all register data and format it for db table useing serializer
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        if "password" in request.data:
            # If the password field is included in the request, use the UserSerializer
            serializer = UserSerializer(user, data=request.data)
        else:
            # If the password field is NOT included, use the UserUpdateSerializer
            serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response({"success": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)