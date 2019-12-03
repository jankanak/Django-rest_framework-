from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from restapp.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
payload_handler=api_settings.JWT_PAYLOAD_HANDLER
encode_handler=api_settings.JWT_ENCODE_HANDLER

User=get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj=User(username="tonu",email="tonu@gmail.com")
        user_obj.set_password("kanakalhassan")
        user_obj.save()
        blogpost=BlogPost.objects.create(user=user_obj,title='kaka',content='greatest footballer')

    def test_single_user(self):
        user_count=User.objects.count()
        self.assertEqual(user_count,1)
    
    def test_single_post(self):
        post_count=User.objects.count()
        self.assertEqual(post_count,1)
    
    def test_get_list(self):
        data={}
        url=api_reverse("api-restapp:post-create")
        response=self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #print(response.data)
    
    def test_post_item(self):
        data={"title":"kaka","content":"greatest footballer"}
        url=api_reverse("api-restapp:post-create")
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_get_item(self):
        blog_post=BlogPost.objects.first()
        data={}
        url=blog_post.get_api_url()
        responsee=self.client.get(url,data,format='json')
        self.assertEqual(responsee.status_code,status.HTTP_200_OK)
        print(responsee.data)
    
    def test_update_item(self):
        blog_post=BlogPost.objects.first()
        data={"title":"rando","content":"ok more content"}
        url=blog_post.get_api_url()
        responsee=self.client.post(url,data,format='json')
        self.assertEqual(responsee.status_code,status.HTTP_401_UNAUTHORIZED)
        responsee=self.client.put(url,data,format='json')
        self.assertEqual(responsee.status_code,status.HTTP_401_UNAUTHORIZED)
        #print(responsee.data)

    def test_update_item_with_user(self):
        blog_post=BlogPost.objects.first()
        print(blog_post.content)
        data={"title":"rando","content":"ok more content"}
        user_obj=User.objects.first()
        payload=payload_handler(user_obj)
        token_rsp=encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT'+token_rsp)
        url=blog_post.get_api_url()
        responsee=self.client.post(url,data,format='json')
        self.assertEqual(responsee.status_code,status.HTTP_401_UNAUTHORIZED)
        print(responsee.data)