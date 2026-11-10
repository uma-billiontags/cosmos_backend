import random
import uuid
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer

class GoogleLoginView(APIView):
    """
    Google authentication with email and password verification.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '').strip()
        name = request.data.get('name', '').strip()

        if not email:
            return Response({"detail": "Email address is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            name = email.split('@')[0].replace('.', ' ').title()

        try:
            user = User.objects.get(email__iexact=email)
            if user.password and user.password.startswith('pbkdf2_'):
                if password and not user.check_password(password):
                    return Response({"detail": "Wrong password. Try again."}, status=status.HTTP_401_UNAUTHORIZED)
            elif password:
                user.set_password(password)
                user.save(update_fields=['password'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password if password else 'Password123!',
                role='Admin' if 'admin' in email.lower() or User.objects.count() == 0 else 'Employee'
            )

        update_fields = ['status']
        user.status = 'online'
        if name and user.name != name:
            user.name = name
            update_fields.append('name')
        user.save(update_fields=update_fields)

        refresh = RefreshToken.for_user(user)

        return Response({
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email not found."}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify password if set
        if password and not user.check_password(password):
            return Response({"detail": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        user.status = 'online'
        user.save(update_fields=['status'])

        return Response({
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class GuestLoginView(APIView):
    """
    Allow external guests to enter directly without signing in.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            name = f"Guest {random.randint(100, 999)}"

        guest_email = f"guest_{uuid.uuid4().hex[:8]}@guest.cosmos.local"
        user = User.objects.create_user(
            email=guest_email,
            name=name,
            password=str(uuid.uuid4()),
            role='Guest'
        )
        user.status = 'online'
        user.save(update_fields=['status'])

        refresh = RefreshToken.for_user(user)

        return Response({
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            "user": UserSerializer(user).data,
            "is_guest": True,
        }, status=status.HTTP_200_OK)

class UserSearchListView(APIView):
    """
    List registered team members for inviting into spaces.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        users = User.objects.filter(is_active=True).exclude(role='Guest')
        if q:
            users = users.filter(Q(name__icontains=q) | Q(email__icontains=q))
        users = users.order_by('name')[:30]
        return Response([{
            'id': str(u.id),
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'status': u.status,
        } for u in users], status=status.HTTP_200_OK)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            request.user.status = 'offline'
            request.user.save(update_fields=['status'])
            # If user was a guest, we can also delete or mark inactive
            if request.user.role == 'Guest':
                request.user.is_active = False
                request.user.save(update_fields=['is_active'])
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
