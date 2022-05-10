from rest_framework import serializers

from news.models import News


class NewsShortSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return obj.comment_counter

    class Meta:
        model = News
        fields = ['id', 'title', 'comments']

class NewsFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'


