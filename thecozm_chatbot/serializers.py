from rest_framework import serializers

from thecozm_chatbot.models import TheCozmChat


class ConversationSerializer(serializers.Serializer):
    role = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = TheCozmChat
        fields = ['role', 'content']

    def get_role(self, obj):
        return "user" if obj.user else "assistant"

    def get_content(self, obj):
        return obj.message

