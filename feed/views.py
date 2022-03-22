from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Feed, Image
from .forms import FeedForm

class FeedListView(LoginRequiredMixin, View):

    def postlist_populated(self, request, context):
        #posts = Post.objects.filter(author__userfollow__followers__in=[request.user.id])#Fix later #For reference
        feeds = Feed.objects.all().order_by('-created_on') #Fix later
        # blog = Blog.objects.filter(is_draft=False) #Fix later
        # result_list = sorted(chain(posts, product, forum, blog),key=attrgetter('created_on'), reverse=True)
        join_paginator = Paginator(feeds,10)
        page = request.GET.get('page', 1)
        
        try:
            join_pagination = join_paginator.page(page)
        except PageNotAnInteger:
            join_pagination = join_paginator.page(1)
        except EmptyPage:
            join_pagination = join_paginator.page(join_paginator.num_pages)

        context["results"] = join_pagination
        context["is_home"] = True

    def get(self, request, *args, **kwargs):
        context={}
        # feed = Feed.objects.all()
        group = request.user.check_in_group()
        self.postlist_populated(request, context)
        # context["feed"] = feed
        context["group"] = group
        if request.htmx:
            return render(request, "feed/snippets/main_body.html", context)
        return render(request, 'feed/feed_list.html', context)
    
    def post(self, request, *args, **kwargs):
        import time
        time.sleep(1)
        context = {}
        form = FeedForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        group = request.user.check_in_group()
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.author_group = group
            new_post.save()

            # new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()
            
        else:
            print(form.errors)
        self.postlist_populated(request, context)
        return render(request, 'feed/snippets/main_body.html', context)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        context={}
        feed = Feed.objects.get(pk=pk)
        feed.addLike(request.user)
        context["result"] = feed
        return render(request,"feed/snippets/like_post_button.html",context)