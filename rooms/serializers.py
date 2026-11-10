from rest_framework import serializers
from .models import Room, Space, SpaceMember

class RoomSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.name')
    active_participants = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'space',
            'type',
            'capacity',
            'description',
            'created_by',
            'created_by_name',
            'active_participants',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_active_participants(self, obj):
        return []

    def validate(self, attrs):
        request = self.context.get('request')
        room_type = attrs.get('type', 'temporary')

        # Only Admins can create permanent rooms
        if room_type == 'permanent' and request and request.user.role != 'Admin':
            raise serializers.ValidationError({"type": "Only Admins can create permanent rooms."})

        return attrs

class SpaceMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    name = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.email')
    user_role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = SpaceMember
        fields = [
            'id',
            'user_id',
            'name',
            'email',
            'user_role',
            'role',
            'joined_at',
        ]
        read_only_fields = ['id', 'user_id', 'name', 'email', 'user_role', 'joined_at']
