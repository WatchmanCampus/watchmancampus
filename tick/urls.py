from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, PreviewTicket, PostDetailView, PostUpdateView, PostDeleteView, \
    PostCreateView, PostListView


urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    # path('register/', TickCreateView, name='register'),
    path('preview/<str:ref>', PreviewTicket, name='preview'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]
