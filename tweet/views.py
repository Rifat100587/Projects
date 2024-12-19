from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from django.http import HttpResponseForbidden
from .forms import TweetForm
# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet_list.html', {'tweets': tweets})

def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

def tweet_edit(request, tweet_id):  # Parameter name matches URL pattern
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

def tweet_delete(request, tweet_id):
    # First check if the tweet exists at all
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    
    # Then check if the user has permission
    if tweet.user != request.user:
        # Handle unauthorized access
        return HttpResponseForbidden("You don't have permission to delete this tweet")
        
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_delete.html', {'tweet': tweet})
