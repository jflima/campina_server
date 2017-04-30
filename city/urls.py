from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from city import views


urlpatterns = [
	url(r'^$', views.CityList.as_view()),
    url(r'^(?P<code>[0-9]+)/$', views.CityDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)