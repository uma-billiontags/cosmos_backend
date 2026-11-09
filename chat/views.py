from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
import uuid
from rooms.models import Room
from accounts.models import User
from accounts.serializers import UserSerializer

def resolve_room(room_id, created_by=None):
    # 1. Try UUID lookup
    try:
        val = uuid.UUID(str(room_id))
        room = Room.objects.filter(id=val).first()
        if room:
            return room
    except (ValueError, AttributeError):
        pass

    # 2. Try by exact name or slug
    room = Room.objects.filter(name__iexact=room_id).first()
    if room:
        return room

    clean_name = str(room_id).replace('-', ' ').replace('_', ' ').title()
    room = Room.objects.filter(name__iexact=clean_name).first()
    if room:
        return room

    # 3. Auto-create if not found so room chat never 404s
    if created_by:
        return Room.objects.create(
            name=clean_name if clean_name else str(room_id),
            type='temporary',
            capacity=20,
            created_by=created_by
        )
    return None

class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = resolve_room(room_id, created_by=request.user)
        if not room:
            return Response([], status=status.HTTP_200_OK)
        messages = Message.objects.filter(room=room, is_direct=False).order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        room = resolve_room(room_id, created_by=request.user)
        text = request.data.get('text', '').strip()
        if not text:
            return Response({"detail": "Message text cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=request.user,
            room=room,
            text=text,
            is_direct=False
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DirectMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        messages = Message.objects.filter(
            is_direct=True
        ).filter(
            (Q(sender=request.user) & Q(recipient=other_user)) |
            (Q(sender=other_user) & Q(recipient=request.user))
        ).order_by('created_at')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        recipient = get_object_or_404(User, id=user_id)
        text = request.data.get('text', '').strip()
        if not text:
            return Response({"detail": "Message text cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            text=text,
            is_direct=True
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatContactsView(APIView):
    """
    Returns available team members in the office to start direct messages with.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teammates = User.objects.exclude(id=request.user.id).order_by('name')
        return Response(UserSerializer(teammates, many=True).data, status=status.HTTP_200_OK)
