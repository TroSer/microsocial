from django.conf.urls import url
from person import views


urlpatterns = [
    url(r'^profile/(?P<person_id>\d+)/$', views.PersonProfileView.as_view(), name='profile'),
]
