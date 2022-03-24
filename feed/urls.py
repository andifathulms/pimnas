from django.urls import path

from .views import(
	AddLike,
    FeedDetailView,
    FeedEditViewHTMX,
    FeedDeleteView,
    AddCommentLike,
    CommentDeleteView,
)

app_name = 'feed'

urlpatterns = [
    path('<int:pk>/like', AddLike.as_view(), name='feed-like'),
    path('<int:pk>/', FeedDetailView.as_view(), name='feed-detail'),
    path('edit/<int:pk>/', FeedEditViewHTMX.as_view(), name='feed-edit'),
    path('delete/<int:pk>/', FeedDeleteView.as_view(), name='feed-delete'),
    path('<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]