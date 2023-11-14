from rest_framework import serializers
from apps.blog.models import Blog
from datetime import datetime


class BlogApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['slug','id', 'title', 'date', 'blog_image','is_blog','is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Format the date field
        date_string = data.get('date', '')
        if date_string:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = date.strftime("%b %d/%Y")
            data['date'] = formatted_date

        # Replace None values with empty strings
        for field in data.keys():
            if data[field] is None:
                data[field] = ""

        return data
    
    
class BlogApiDerailsListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','slug','title','blog_image','date','description','is_active','og_image','meta_image_title','meta_title','meta_description','meta_keyword']


    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Format the date field
        date_string = data.get('date', '')
        if date_string:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = date.strftime("%b %d/%Y")
            data['date'] = formatted_date

        # Replace None values with empty strings
        for field in data.keys():
            if data[field] is None:
                data[field] = ""

        return data


