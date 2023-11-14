from rest_framework import serializers
from apps.blog.models import Blog


class BlogApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','blog_image','date','description','is_active','og_image','meta_image_title','meta_title','meta_description','meta_keyword']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


