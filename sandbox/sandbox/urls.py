from django.conf.urls import url
from main.views import home, say_hello, post_it, post_file, post_name


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^say/$', say_hello, name='say_hello'),
    url(r'^post_it/$', post_it, name='post_it'),
    url(r'^post_file/$', post_file, name='post_file'),
    url(r'^post-name/$', post_name, name='post_name'),
]
