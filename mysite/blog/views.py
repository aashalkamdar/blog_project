from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from blog.models import Post , Comment
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

#here we dont use decorators because decorators really only work in function based views and not class based views
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

        # #python like code  for sql. lte means less than or equal to . this defines a query set which allows to display
        # the posts in a descending order . the - is imperative. it allows the posts to be displayed in descending order or else
        # we would have oldest posts before


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post



class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post

    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

###############################################
###############################################
@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            #in models.py Comment has an attribute called post which is linked by Foreignkey to Post . this tells us to save comment.post by making it equal to post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html', {'form': form})

    #login is requred to post on a comment . we taake in request and pk (primary key) as parameters.when we go to post_ detail page
    # and click on comment itll take in our request and pk which links the comment to the post
    # then we say 'either get the post object or the 404 page' , pass in the Post mpdel aND PK

@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
