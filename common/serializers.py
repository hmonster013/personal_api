from rest_framework import serializers

from common.models import File, Links, Skills, Contact

class FileSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'public_id', 'resource_type', 'file_type', 'full_url', 'uploaded_at']

    def get_full_url(self, obj):
        return obj.get_full_url()

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'icon', 'name']
        
class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ['id', 'name', 'title', 'url', 'icon']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']

    def create(self, validated_data):
        # Lấy thông tin IP và User Agent từ request context
        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = self.get_client_ip(request)
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')

        return super().create(validated_data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip