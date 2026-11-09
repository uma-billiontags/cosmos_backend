from django.urls import path
from .views import (
    SpaceListView,
    RoomListCreateView,
    RoomDetailDeleteView,
    RoomTokenView,
    RoomModerationView,
    EndRoomView,
)
from chat.views import RoomMessagesView

urlpatterns = [
    path('spaces/', SpaceListView.as_view(), name='space-list-create'),
    path('', RoomListCreateView.as_view(), name='room-list-create'),
    path('<uuid:room_id>/', RoomDetailDeleteView.as_view(), name='room-detail-delete'),
    path('<uuid:room_id>/token/', RoomTokenView.as_view(), name='room-token'),
    path('<str:room_id>/messages/', RoomMessagesView.as_view(), name='room-messages'),
    path('<uuid:room_id>/participants/<str:participant_identity>/<str:action>/', RoomModerationView.as_view(), name='room-moderate'),
    path('<uuid:room_id>/end/', EndRoomView.as_view(), name='room-end'),
]
