from rest_framework import serializers

from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    shared_with = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = ('id', 'title', 'content_type', 'text', 'audio', 'video', 'owner', 'shared_with', 'created_at', 'updated_at')

        extra_kwargs = {
            'text': {'write_only': True},
            'audio': {'write_only': True},
            'video': {'write_only': True},
        }

    def validate(self, data):
        print("data is :==> ",data)
        if not data.get('content_type'):
            raise serializers.ValidationError({"content_type": "content_type is required [text, audio, video]"})
        if data['content_type'] == 'text' and not data.get('text'):
            raise serializers.ValidationError({"text": "'text' is required for content_type 'text'"})
        if data['content_type'] == 'audio' and not data.get('audio'):
            raise serializers.ValidationError({"audio": "audio is required for content_type 'audio'"})
        if data['content_type'] == 'video' and not data.get('video'):
            raise serializers.ValidationError({"video": "video is required for content_type 'video'"})
        data['owner'] = self.context['request'].user
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        c_type = representation['content_type']
        if c_type == 'text':
            representation['content'] = instance.text
        else:
            c_url = instance.audio.url if c_type == 'audio' else instance.video.url
            representation['content'] = self.context['request'].build_absolute_uri(c_url)
        return representation