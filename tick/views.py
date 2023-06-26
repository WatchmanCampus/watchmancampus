from django.shortcuts import render, redirect, get_object_or_404
from .forms import TickRegisterForm
from PIL import Image, ImageFont, ImageDraw
from django.contrib import messages
from .utils import generate_ticket, my_random_string, email_sending
from .models import Tick, Post


# from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



def home_page(request):
    return render(request, "tick/index.html", {})

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
            return redirect('payment', new.pk)
    else:
        form = TickRegisterForm()
    context = {
        "post": post,
        "form": form,
    }

    return render(request, 'tick/post_detail.html', context)

def Payment(request, pk):
    ticket = Tick.objects.get(pk=pk)
    if request.method == 'POST':
        pass
    context = {"ticket": ticket}

    return render(request, 'tick/payment.html', context)
    
    
# def PostDetailView(request, pk):
#     post = Post.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = TickRegisterForm(request.POST)
#         if form.is_valid():
#             ref = my_random_string()
#             new = form.save(commit=False)  # Create, but don't save the new instance.
#             new.ref = ref
#             new.post = post
#             new.save()
#             form.save_m2m()
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             email = form.cleaned_data.get('email')
#             gender = form.cleaned_data.get('gender')
#             diocese = form.cleaned_data.get('diocese')

#             ref = generate_ticket(first_name, last_name, gender, diocese, ref)
#             response = email_sending(
#                 to_mail=email, 
#                 firstname=first_name, 
#                 lastname=last_name, 
#                 location=post.location, 
#                 time=post.start_date,
#                 ref=ref

#             )
#             if response == True:
#                 return redirect('preview', ref=ref)
#             else:
#                 return redirect('preview', ref=ref)
#     else:
#         form = TickRegisterForm()

#     context = {
#         "post": post,
#         "form": form,
#     }
#     return render(request, 'tick/post_detail.html', context)


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
