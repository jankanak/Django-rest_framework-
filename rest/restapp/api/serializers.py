from rest_framework  import serializers
from restapp.models import BlogPost

class BlogPostSerializers(serializers.ModelSerializer):
    url=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=BlogPost
        fields=[
            'url',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields=['id','user']

    def get_url(self,obj):
        request=self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self,value):
        qs=BlogPost.objects.filter(title__iexact=value)

        if self.instance:
            qs=qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("this title has been already taken")
        return value 