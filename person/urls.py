from django.conf.urls import url
from person import views


urlpatterns = [
    url(r'^profile/(?P<person_id>\d+)/$', views.PersonProfileView.as_view(), name='profile'),
    url(r'^settings/$', views.PersonEditView.as_view(), name='profile_edit'),
    url(
        r'^friends/$',
        views.UserFriendsView.as_view(),
        name='user_friends'
    ),
    url(
        r'^friends/incoming/$',
        views.UserIncomingView.as_view(),
        name='user_incoming'
    ),
    url(
        r'^friends/outcoming/$',
        views.UserOutcomingView.as_view(),
        name='user_outcoming'
    ),
    url(
        r'^api/friends/$',
        views.FrienshipAPIView.as_view(),
        name='user_friendship_api'
    ),
]
