from rest_framework import generics,mixins
from restapp.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializers
from django.db.models import Q


class BlogPostApiView(mixins.CreateModelMixin ,generics.ListAPIView):
    lookup_field='pk'
    serializer_class=BlogPostSerializers
    permission_classes=[IsOwnerOrReadOnly]

    def get_queryset(self):
        qs=BlogPost.objects.all()
        query=self.request.GET.get("q")

        if query is not None:
            qs=qs.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
        return qs


    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self,*args,**kargs):
        return {"request":self.request}

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field='pk'
    serializer_class=BlogPostSerializers

    def get_queryset(self):
        return BlogPost.objects.all()
    
    def get_serializer_context(self,*args,**kargs):
        return {"request":self.request}

