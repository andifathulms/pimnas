from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from .models import Feed, Comment, Image
from .forms import FeedForm, CommentForm

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

class FeedDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post =  Feed.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        
        is_post_like = False
        if request.user in post.likes.all():
            is_post_like = True

        comment_list = []
        for comment in comments:
            is_like = False
            if request.user in comment.likes.all():
                is_like = True

            comment_list.append((comment,is_like))

        context = {
            'post': post,
            'result': post,
            'form': form,
            'comments': comments,
            'is_post_like' : is_post_like,
        }        
        return render(request, 'feed/feed_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        
        post = Feed.objects.get(pk=pk)
        form = CommentForm(request.POST)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            # new_comment.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_comment.image.add(img)

            new_comment.save()
        else:
            print(form.errors)

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        print(context)
        return render(request, 'feed/snippets/feed_detail_new_comment.html', context)

class FeedEditViewHTMX(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request, pk, *args, **kwargs):
        post = Feed.objects.get(pk=pk)


        context = {
            'post': post
        }

        return render(request, 'feed/snippets/feed_detail_inline_editing.html', context)
    def put(self, request, pk, *args, **kwargs):
        post = Feed.objects.get(pk=pk)
        form = FeedForm(request.PUT, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            print(request.PUT)

            # post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                post.image.add(img)

            #post.save()
            
        else:
            print(form.errors)

        return render(request, 'feed/feed_detail_tweet.html', {})

class FeedDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feed
    template_name = 'feed/feed_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        post = Feed.objects.get(pk=post_pk)
        context={}
        context["result"] = comment
        
        return render(request, 'feed/snippets/comment_like.html', context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'feed/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('feed:feed-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        context={}
        feed = Feed.objects.get(pk=pk)
        feed.addLike(request.user)
        context["result"] = feed
        return render(request,"feed/snippets/like_post_button.html",context)