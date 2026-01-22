import logging

from pydantic import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .serializers import RegisterSerializer, LoginSerializer
from .services import validate_token
from schemas.auth import UserCreateSchema

logger = logging.getLogger("auth")


# --------- Register View ---------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # 🔥 Throttle: 3 requests per minute
    throttle_scope = "register"

    def post(self, request, *args, **kwargs):
        logger.info("Register attempt")
        try:
            # ✅ Step 1: Validate using Pydantic
            schema = UserCreateSchema(**request.data)

        except ValidationError as e:
            return Response(
                {"errors": e.errors()},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        serializer = self.get_serializer(data=schema.model_dump())
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


# --------- Login & Token Validation View ---------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def get_throttles(self):
        """
        POST  -> login (5/min)
        GET   -> token validation (60/min)
        """
        if self.request.method == "POST":
            self.throttle_scope = "login"
        else:
            self.throttle_scope = "token_validate"

        return super().get_throttles()

    # --------- Token Validation ---------
    def get(self, request):
        logger.debug("Token validation request")

        try:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.split(" ")[1]

            user = validate_token(token)

            if not user:
                logger.warning("Invalid token provided")
                return Response(
                    {"detail": "Invalid token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            logger.info("Token validated", extra={"user_id": user.id})

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.exception("Token validation failed")
            return Response(
                {"detail": "Authentication failed"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    # --------- Login ---------
    def post(self, request):
        logger.info("Login attempt")

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        logger.info(
            "Login successful",
            extra={"user_id": user.id, "email": user.email}
        )

        return Response(
            {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK
        )
