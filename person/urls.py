from django.conf.urls import url
from person import views


urlpatterns = [
    url(r'^users/profile/(?P<person_id>\d+)/$', views.PersonProfileView.as_view(), name='profile'),
    url(r'^settings/$', views.PersonEditView.as_view(), name='profile_edit'),
]
