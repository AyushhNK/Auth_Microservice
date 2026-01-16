import proto.auth_pb2 as auth_pb2
import proto.auth_pb2_grpc as auth_pb2_grpc
import jwt
from .models import User


SECRET = "5ahp8kseKOVB_w"


def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except Exception:
        return None

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def ValidateToken(self, request, context):
        user = validate_token(request.token)
        if not user:
            return auth_pb2.UserResponse(is_active=False)
        return auth_pb2.UserResponse(
            user_id=user.id,
            email=user.email,
            is_active=user.is_active
            )