from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.ReadOnlyField(source='sender.id')
    sender_name = serializers.ReadOnlyField(source='sender.name')
    sender_role = serializers.ReadOnlyField(source='sender.role')
    recipient_id = serializers.ReadOnlyField(source='recipient.id')
    recipient_name = serializers.ReadOnlyField(source='recipient.name')
    room_id = serializers.ReadOnlyField(source='room.id')
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender_id',
            'sender_name',
            'sender_role',
            'room',
            'room_id',
            'recipient',
            'recipient_id',
            'recipient_name',
            'text',
            'is_direct',
            'timestamp',
            'created_at',
        ]
        read_only_fields = ['id', 'sender_id', 'sender_name', 'sender_role', 'timestamp', 'created_at']
