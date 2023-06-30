from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
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


@api_view(["POST"])
def register_user(request):
    # get all register data and format it for db table useing serializer
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
