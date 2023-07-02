from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, PreviewTicket, PostDetailView, PostUpdateView, PostDeleteView, \
    PostCreateView, PostListView, Payment, verify_transaction


urlpatterns = [
    path('', home_page, name='home-page'),
    path('posts', PostListView.as_view(), name='home'),
    # path('register/', TickCreateView, name='register'),
    path('preview/<int:ticket_id>', PreviewTicket, name='preview'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('ticket/<int:ticket_id>/payment', Payment, name='ticket-payment'),
    path(
        "verify/transaction/<slug:transaction_id>/",
        verify_transaction,
        name="verify-transaction",
    ),
]
