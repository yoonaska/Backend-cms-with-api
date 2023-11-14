from rest_framework import serializers
from apps.news.models import News


class NewsApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','title','news_image','url_link','is_active']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


