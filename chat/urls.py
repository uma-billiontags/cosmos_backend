from django.urls import path
from .views import RoomMessagesView, DirectMessagesView, ChatContactsView

urlpatterns = [
    path('rooms/<str:room_id>/messages/', RoomMessagesView.as_view(), name='room-messages'),
    path('direct/<uuid:user_id>/', DirectMessagesView.as_view(), name='direct-messages'),
    path('contacts/', ChatContactsView.as_view(), name='chat-contacts'),
]
