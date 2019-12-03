from django.conf.urls import url
from .views import BlogPostRudView,BlogPostApiView
app_name = 'restapp'

urlpatterns=[
    url(r'^(?P<pk>\d+)/$',BlogPostRudView.as_view(),name='post-rud'),
    url(r'^$',BlogPostApiView.as_view(),name='post-create'),
]