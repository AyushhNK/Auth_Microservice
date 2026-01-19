import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse as httpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from .services import validate_token

logger = logging.getLogger("auth")

# --------- Register View ---------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Register attempt")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        logger.info(
            "User registered successfully",
            extra={"user_id": user.id, "email": user.email}
        )

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


# --------- Login View ---------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.debug("Token validation request")

        try:
            token = request.headers.get("Authorization", "").split(" ")[1]
            user = validate_token(token)

            if not user:
                logger.warning("Invalid token provided")
                return Response(
                    {"detail": "Invalid token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            logger.info(f"Token validated for user_id={user.id}")

            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Token validation failed")
            return Response(
                {"detail": "Authentication failed"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        logger.info("Login attempt")

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        logger.info(
            "Login successful",
            extra={"user_id": user.id, "email": user.email}
        )

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)

