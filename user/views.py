
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from user.models import User, UserReview
from user.utils import get_summary


class UserPublicView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'user/public_user.html'

    def get(self, request, key):
        try:
            user = User.objects.get(key=key)
            reviews = UserReview.objects.filter(target=user).order_by('-created')
            summary = get_summary(user)
            if user != request.user:
                user.views += 1
                user.save()
            return render(request, self.template_name, {
                "title": "Overview Real Estate",
                "summary": summary,
                "reviews": reviews,
                "user": user
            })
        except User.DoesNotExist:
            return HttpResponseBadRequest("Not found")
