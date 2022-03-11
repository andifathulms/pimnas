from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View

class FeedListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'feed/feed_list.html', context)
