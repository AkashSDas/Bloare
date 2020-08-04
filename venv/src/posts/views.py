from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormMixin

from comments.forms import CommentForm
from comments.models import Comment
from profiles.models import Profile

from .models import Post

# User model
User = get_user_model()


# ****** Post List View ******
class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


# ****** Post Create View ******
# Template name == 'post_form.html
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Overriding the form_valid method
    # This is so that users can post only through there accounts.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


# ****** Post Detail View ******
# Template name == 'post_detail.html
class PostDetailView(DetailView, FormMixin):
    model = Post
    form_class = CommentForm

    def get_absolute_url(self, id):
        instance = Post.objects.get(id=id)
        return reverse('post_detail', args=[instance.id])

    # Getting the comment form
    def get_form(self, **kwargs):
        pk = int(self.request.path.split('/')[3])  # To get post's id
        instance = Post.objects.get(pk=pk)
        form = super(PostDetailView, self).get_form(**kwargs)
        initial_data = {
            'content_type': instance.get_content_type,
            'object_id': instance.id,
        }
        form.initial = initial_data
        return form

    # Getting the context object
    def get_context_data(self, **kwargs):
        pk = kwargs['object'].pk
        instance = Post.objects.get(pk=pk)

        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = instance.comments
        # context['comments'] = Comment.objects.filter_by_instance(instance)

        context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):

        # User can only reply when they are logged in
        if not request.user.is_authenticated:
            return redirect('login')

        # We can use the below line to create a CommentForm but to make `comment
        # app` more independent we are going to use the get_form() method of
        # PostDetailView class(i.e. this class).
        # comment_form = CommentForm(request.POST or None, initial=initial_data)

        # Getting the comment form
        comment_form = self.get_form()

        if comment_form.is_valid():
            c_type = comment_form.cleaned_data.get('content_type')
            model_name = c_type.split('|')[1].strip()
            content_type = ContentType.objects.get(model=model_name)
            obj_id = comment_form.cleaned_data.get('object_id')
            content_data = comment_form.cleaned_data.get('content')
            parent_obj = None
            try:
                # If parent_id is present then this comment is actually
                # the reply of the comment of whose parent_id is found.
                parent_id = int(request.POST.get('parent_id'))
            except:
                # If parent_id is not present then it means that this is
                # a comment.
                parent_id = None

            if parent_id:
                parent_queryset = Comment.objects.filter(id=parent_id)
                if parent_queryset.exists() and parent_queryset.count() == 1:
                    parent_obj = parent_queryset.first()

            # Creating a new comment if parent_id=None or new reply to the
            # comment of whose parent_id we got from the POST request.
            new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                parent=parent_obj,
            )

        url = self.get_absolute_url(kwargs['pk'])
        return redirect(url)


# ****** Post Update View ******
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_update_form.html'

    # Overriding the form_valid method
    # This is so that users can update only their posts.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

    # Overriding the test_func method
    # This is to check whether the update request is from the author
    # of that post or not.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# ****** Post Delete View ******
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts/home/'

    # Overriding the test_func method
    # This is to check whether the delete request is from the author
    # of that post or not.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# ****** User's Post List View ******
# All the posts related to a specific user.
class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # Overriding the get_queryset method
    # This is to query specific user's posts in custom way.
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('date_posted')


# ****** Author's Profile View ******
# This profile will be visible to all other users
""" 
    NOTE: This profile is different from individual User's Profile.
    
    1) User's Profile:
    - User's Profile is visible from that user's account only.
    - User can update there profile data from their User's Profile.
 
    2) Author's Profile:
    - Author's Profile is visible to all other users.
"""


def display_author_profile_view(request, username, pk):
    # Here (username == Author's username) and (pk == Post's primary key)

    user = User.objects.filter(username=username).first()
    context = {
        'profile': Profile.objects.filter(user=user).first(),
        'post': Post.objects.filter(pk=pk).first(),
    }
    return render(request, 'posts/display_author_profile.html', context)


# ****** Like Post View ******
@login_required
def liked_post_view(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    # Checking if user has already liked or disliked the post
    already_liked = post.likes.filter(id=request.user.id).exists()
    already_disliked = post.dislikes.filter(id=request.user.id).exists()

    if not already_liked and not already_disliked:
        post.likes.add(request.user)
    elif already_liked and not already_disliked:
        post.likes.remove(request.user)
    elif not already_liked and already_disliked:
        post.dislikes.remove(request.user)
        post.likes.add(request.user)

    post_url = post.get_absolute_url()
    return redirect(post_url)


# ****** Dislike Post View ******
@login_required
def disliked_post_view(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    # Checking if user has already liked or disliked the post
    already_liked = post.likes.filter(id=request.user.id).exists()
    already_disliked = post.dislikes.filter(id=request.user.id).exists()

    if not already_liked and not already_disliked:
        post.dislikes.add(request.user)
    elif already_disliked and not already_liked:
        post.dislikes.remove(request.user)
    elif not already_disliked and already_liked:
        post.likes.remove(request.user)
        post.dislikes.add(request.user)

    post_url = post.get_absolute_url()
    return redirect(post_url)
