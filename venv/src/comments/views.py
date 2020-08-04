from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import DeleteView, UpdateView

from posts.models import Post

from .models import Comment


# ****** Comment Update View ******
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'comments/comment_update_form.html'

    def get_absolute_url(self, *args, **kwargs):
        comment = self.get_object()
        instance = comment.content_object
        return reverse('post_detail', args=[instance.id])

    def get_success_url(self):
        return self.get_absolute_url()

    def get_queryset(self):
        comment = Comment.objects.filter(pk=self.kwargs.get('pk'))
        return comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CommentUpdateView, self).form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


# ****** Comment Delete View ******
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_absolute_url(self):
        comment = self.get_object()
        instance = comment.content_object
        return reverse('post_detail', args=[instance.id])

    def get_success_url(self):
        return self.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_queryset(self):
        comment = Comment.objects.filter(pk=self.kwargs.get('pk'))
        return comment
