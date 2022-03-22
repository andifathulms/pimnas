from django.urls import path

from .views import(
	AddLike,
)

app_name = 'feed'

urlpatterns = [
    path('<int:pk>/like', AddLike.as_view(), name='feed-like'),
]