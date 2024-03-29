from django.shortcuts import render, redirect, get_object_or_404
from .forms import TickRegisterForm, PaymentForm
from django.contrib import messages
from .utils import generate_ticket, my_random_string, email_sending
from .models import Tick, Post, Transaction, Hostel
from .payments import verify_rave, initiate_rave_url
from PIL import Image, ImageFont, ImageDraw
# from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def home_page(request):
    return render(request, "tick/index.html", {})


def home(request):
    return render(request, "tick/home.html", {"title": "home"})


def PostDetailView(request, pk):
    post = Post.objects.get(pk=pk)
    ticker = Tick.objects.first()
    if request.method == "POST":
        form = TickRegisterForm(request.POST)
        if form.is_valid():
            ref = my_random_string()
            ticket = form.save(
                commit=False
            )  # Create, but don't save the ticket instance.
            ticket.ref = ref
            ticket.post = post
            ticket.save()
            return redirect("preview", ticket.id)
            # return redirect("ticket-payment", ticket.pk)
        else:
            errors = form.errors
            print(errors)
    else:
        form = TickRegisterForm()
    context = {
        "ticket": ticker,
        "post": post,
        "form": form,
    }

    return render(request, "tick/post_detail.html", context)


def Payment(request, ticket_id):
    ticket = get_object_or_404(Tick, id=ticket_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction_ref = my_random_string()
            transaction, created = Transaction.objects.update_or_create(
                ticket=ticket,
                defaults={
                    "transaction_ref": transaction_ref,
                    "payment_provider": "payment_rave",
                    "total_price": ticket.post.price,
                },
            )
            server_url = "localhost:8000"  # get_secret("SERVER_URL")
            callback_url = f"{server_url}/ticket/verify/transaction/{transaction.id}"
            response = initiate_rave_url(
                email=ticket.email,
                amount=int(
                    transaction.total_price
                ),  # convert to lowest unit and integer
                transaction_ref=transaction_ref,
                currency="NGN",
                callback_url=callback_url,
            )
            try:
                rave_url = response["data"]["link"]
                return redirect(rave_url)
            except Exception:
                messages.warning(request, f"Your transaction {response['message']}")
                return redirect("post-detail", ticket.id)
    else:
        form = PaymentForm()

    context = {"ticket": ticket, "form": form}

    return render(request, "tick/payment.html", context)


def verify_transaction(request, transaction_id):
    transaction_ref = request.GET.get("trxref")
    transaction = get_object_or_404(
        Transaction, id=transaction_id, transaction_ref=transaction_ref
    )
    response = verify_transaction(transaction_ref=transaction_ref)
    if (
        response["data"]["status"] == "successful"
        and response["data"]["amount"] == transaction.total_price
        and response["data"]["currency"] == "NGN"
    ):
        transaction.transaction_status = "Payment Completed"
        transaction.transaction_description = response["data"]["message"]
        transaction.save()

    return redirect("preview", transaction.ticket.id)


def PreviewTicket(request, ticket_id):
    ticket = Tick.objects.get(id=ticket_id)
    try:
        hostel = Hostel.objects.filter(gender_type=ticket.gender, hostel_class='Regular', is_available=True)[0]
        hostel.booked.add(ticket.id)
        hostel.rooms_available -= 1
        hostel.save()

        img = Image.open('hilltop.jpg')
        font = ImageFont.truetype("Arial.ttf", 30)
        edited = ImageDraw.Draw(img)
        edited.text((300, 300), f'{ticket.first_name} {ticket.last_name}', (247, 19, 7), font=font)
        edited.text((300, 350), ticket.diocese, (247, 19, 7), font=font)
        edited.text((300, 400), hostel.name, (247, 19, 7), font=font)
        img_name = f'media/{ticket.first_name}-{ticket.ref}.jpg'
        img.save(img_name)
        # imgy = Image.open(img_name)
        ticket.img = f'{ticket.first_name}-{ticket.ref}.jpg'
        ticket.save()
        try:
            email_sent = email_sending(
                to_mail=ticket.email,
                firstname=ticket.first_name,
                lastname=ticket.last_name,
                location=ticket.post.venue,
                time=ticket.post.start_date,
                ref=ticket.ref,
            )
            if email_sent is True:
                messages.success(request, f"Your have successfully registered for hilltop please check your mail for more info")
                return redirect("post-detail", ticket.id)
        except:
            messages.error(request, f"There was a problem processing your ticket to your mail, contact support")
            return redirect("post-detail", ticket.id)

        return render(request, "tick/preview.html", {"ticket": ticket})
    except Exception as e:
        print(str(e))
        messages.error(request, f"There was a problem with your request")
        return redirect("post-detail", ticket.id)


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


class PostListView(ListView):
    model = Post
    template_name = "tick/home.html"
    context_object_name = "posts"
    ordering = ["-start_date"]
    paginate_by = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "description"]

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
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
