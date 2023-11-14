from rest_framework import serializers
from apps.seo.models import SeoManagement


class SeoManagementApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = SeoManagement
        fields = ['id','og_image','meta_image_title','meta_title','meta_description','meta_keyword','is_active',]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


