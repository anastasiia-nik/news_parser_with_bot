from rest_framework import serializers

from news.models import News, Tags


class NewsShortSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return obj.comment_counter

    class Meta:
        model = News
        fields = ['id', 'title', 'comments', 'slug']

class NewsFullSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_tags(self, obj):
        return obj.get_tags

    def get_category(self, obj):
        return obj.get_category

    def get_author(self, obj):
        return obj.get_author

    def create(self, validated_data):
        validated_data['category_id'] = 1
        return News.objects.create(**validated_data)

    class Meta:
        model = News
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'tag',]
