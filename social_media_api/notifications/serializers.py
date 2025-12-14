# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor_username",
            "verb",
            "target_object_id",
            "timestamp",
            "is_read",
        ]
        read_only_fields = ["actor_username", "timestamp"]
