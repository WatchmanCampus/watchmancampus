from django.shortcuts import render, get_object_or_404, redirect


def home_page(request):
    return render(request, "pages/home_page.html", {})
