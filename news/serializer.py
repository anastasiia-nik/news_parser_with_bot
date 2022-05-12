from rest_framework import serializers

from news.models import News, Tags


class NewsShortSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return obj.comment_counter

    class Meta:
        model = News
        fields = ['id', 'title', 'comments']

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

    class Meta:
        model = News
        fields = '__all__'

# class TagSerializer(serializers.ModelSerializer):
#     news = serializers.SerializerMethodField()
#
#     def get_news_id(self, obj):
#         return obj.get_news_id
#
#     def get_tags_title(self, obj):
#         return obj.get_news_title
#
#     class Meta:
#         model = Tags
#         fields = ['id', 'tag', 'news']
