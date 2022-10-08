from django.shortcuts import render, redirect, get_object_or_404
from .forms import TickRegisterForm
from PIL import Image, ImageFont, ImageDraw
from django.contrib import messages
from .utils import generate_ticket, my_random_string, email_sending
from .models import Tick, Post


# from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


def home(request):
    return render(request, 'tick/home.html', {'title': 'home'})


def PostDetailView(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = TickRegisterForm(request.POST)
        if form.is_valid():
            ref = my_random_string()
            new = form.save(commit=False)  # Create, but don't save the new instance.
            new.ref = ref
            new.post = post
            new.save()
            form.save_m2m()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            diocese = form.cleaned_data.get('diocese')

            ref = generate_ticket(first_name, last_name, gender, diocese, ref)
            response = email_sending(
                to_mail=email, 
                firstname=first_name, 
                lastname=last_name, 
                location=post.location, 
                time=post.start_date,
                ref=ref

            )
            if response == True:
                return redirect('preview', ref=ref)
            else:
                return redirect('preview', ref=ref)
    else:
        form = TickRegisterForm()

    context = {
        "post": post,
        "form": form,
    }
    return render(request, 'tick/post_detail.html', context)


def PreviewTicket(request, ref):
    ticket = Tick.objects.get(ref=ref)
    # if error == True:
    #     messages.warning(request, f'Failed to send ticket to {ticket.email}, please ensure you download your ticket below')
    # else:
    #     messages.success(request, f'Success. A ticket was sent to {ticket.email}')

    return render(request, 'tick/preview.html', {'ticket': ticket})


class PostListView(ListView):
    model = Post
    template_name = 'tick/home.html'
    context_object_name = 'posts'
    ordering = ['-start_date']
    paginate_by = 10


# class PostDetailView(DetailView):
#     model = Post
#     context_object_name = 'post'


# def PostDetailView(request):
#     # user = get_object_or_404(User, username=request.user)
#     if request.method == "POST":
#         form = TickRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             FeedPost.objects.create(
#                 author=request.user,
#                 message=form.cleaned_data["message"],
#                 image=form.cleaned_data["image"],
#                 # is_private=form.cleaned_data["is_private "],
#                 # category_tags = form.cleaned_data['category_tags'],
#             )
#             messages.info(request, "Your request has been sent.")
#             return redirect("home")
#     else:
#         form = FeedPostCreateForm()

#     queryset = FeedPost.objects.all()
#     paginator = Paginator(queryset, 1)
#     page = request.GET.get("page", 1)
#     try:
#         paginated_queryset = paginator.page(page)
#     except PageNotAnInteger:
#         paginated_queryset = paginator.page(1)
#     except EmptyPage:
#         paginated_queryset = paginator.page(paginator.num_pages)
#     context = {
#         "post": paginated_queryset,
#         "form": form,
#     }

#     return render(request, "post/user_feed.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class UserPostListView(ListView):
#     model = Post
#     template_name = 'blog/user_posts.html'
#     context_object_name = 'post'
#     paginate_by = 5

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')
