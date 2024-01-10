from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Trade, Comment
from .forms import BlogPostForm, CommentForm
from PIL import Image, ImageDraw, ImageFont
import base64
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib import messages


def initialise_blog_context(request, posts):
    posts_per_box = 1
    posts_sets = []

    start = 0
    all_post_ids = []  # New list to store all post IDs

    for i in range(3):
        if start < len(posts):
            posts_sets.append(posts[start:start + posts_per_box])
            start += posts_per_box
        else:
            posts_sets.append([])

    remaining_posts = posts.exclude(id__in=[post.id for posts_set in posts_sets for post in posts_set])

    # Initialise individual_like_counts outside the loop
    individual_like_counts = {}

    total_like_count = 0
    for post_set in posts_sets:
        for post in post_set:
            like_count = post.likes.count()
            individual_like_counts[post.id] = like_count  # Store like count for each post
            total_like_count += like_count
            all_post_ids.append(post.id)  # Add post ID to the list

    # Get like counts for remaining posts
    for post in remaining_posts:
        like_count = post.likes.count()
        individual_like_counts[post.id] = like_count
        total_like_count += like_count
        all_post_ids.append(post.id)  # Add remaining post ID to the list

    # Update the total like count in the session after the calculation
    request.session['total_like_count'] = total_like_count

    return {
        'posts_sets': posts_sets,
        'remaining_posts': remaining_posts,
        'individual_like_counts': individual_like_counts,
        'like_count': like_count,
        'all_post_ids': all_post_ids,  # Add the list of all post IDs
    }
    
@login_required
def view_post(request, post_id):
    blog_post_form = BlogPostForm()
    all_posts = BlogPost.objects.order_by('-timestamp')
    # Retrieve like_counts from session

    context = initialise_blog_context(request, all_posts)
    context.update({
        'blog_post_form': blog_post_form,
        'user_name': request.user.username if request.user.is_authenticated else None,
    })

    post = get_object_or_404(BlogPost, pk=post_id)
    context['post'] = post

    if request.method == 'POST':
        # Check if the form is submitted for adding a comment
        if 'add_comment' in request.POST:
            comment_text = request.POST.get('comment', '')
            if comment_text:
                Comment.objects.create(post=post, user=request.user, content=comment_text)
                # Redirect to the same post after adding a comment
                return redirect('view_post', post_id=post_id)

    return render(request, 'blog.html', context)

@require_POST
def like_toggle(request):
    object_id = request.POST.get('object_id')
    blog_post = get_object_or_404(BlogPost, id=object_id)

    # Check if the user has already liked the object
    user_has_liked = blog_post.likes.filter(id=request.user.id).exists()

    # Toggle like status
    if user_has_liked:
        blog_post.likes.remove(request.user)
    else:
        blog_post.likes.add(request.user)


    # Update the like count in the session for the specific post
    like_count = blog_post.likes.count()
    request.session[f'post_like_count_{object_id}'] = like_count

    # Calculate the total like count based on individual post counts
    total_like_count = sum(request.session.get(f'post_like_count_{post.id}', 0) for post in BlogPost.objects.all())

    # Update the total like count in the session
    request.session['total_like_count'] = total_like_count

    # Update user_like_status after toggling like status
    user_like_status = "liked" if blog_post.likes.filter(id=request.user.id).exists() else "unliked"

    # Return the updated like count and the user's like status
    return JsonResponse({'like_count': like_count, 'user_like_status': user_like_status, 'total_like_count': total_like_count})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    messages.success(request, 'Comment Added!')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect('view_post', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog.html', {'form': form})

class BlogView(View):
    blog = 'blog.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        blog_post_form = BlogPostForm()
        all_posts = BlogPost.objects.order_by('-timestamp')

        posts_per_box = 1
        posts_sets = []

        start = 0
        individual_like_counts = {}  # Dictionary to store individual like counts
        
        # Set a default value for like_count
        like_count = 0

        for i in range(3):
            if start < len(all_posts):
                posts_sets.append(all_posts[start:start + posts_per_box])
                start += posts_per_box
            else:
                posts_sets.append([])

        remaining_posts = all_posts.exclude(id__in=[post.id for posts_set in posts_sets for post in posts_set])

        # Initialise individual_like_counts outside the loop
        individual_like_counts = {}

        total_like_count = 0
        for post_set in posts_sets:
            for post in post_set:
                like_count = post.likes.count()
                individual_like_counts[post.id] = like_count  # Store like count for each post
                total_like_count += like_count

        # Update the total like count in the session after the calculation
        request.session['total_like_count'] = total_like_count

        context = {
            'posts_sets': posts_sets,
            'remaining_posts': remaining_posts,
            'individual_like_counts': individual_like_counts,  # Pass individual like counts to the template
            'like_count': like_count,
            'blog_post_form': blog_post_form,
            'user_name': request.user.username if request.user.is_authenticated else None,
        }

        return render(request, self.blog, context)


    def post(self, request, *args, **kwargs):
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        messages.success(request, 'Post Created!')
        if blog_post_form.is_valid():
            new_post = blog_post_form.save(commit=False)
            new_post.user = request.user

            # Validate required fields
            if not new_post.title or not new_post.content:
                # Handle form validation errors
                errors = blog_post_form.errors
                return render(request, self.blog, {'error': 'Form validation failed', 'errors': errors})

            # If trade_image is present, process it
            trade_image = request.FILES.get('trade_image')

            # Save the new post
            new_post.save()

            return redirect('blog')  # Redirect to the blog page after successful post

        # If form is not valid, render the page with errors
        return render(request, self.blog, {'error': 'Invalid form submission'})
    
    def get_like_count(self, post):
        return Like.objects.filter(liked=self).count()
    
    # Function to generate trade image
    def generate_trade_image(trade_details):
        # Create a blank image
        image = Image.new("RGB", (400, 200), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Add text to the image
        draw.text((10, 10), f"Selected Trade: {trade_details['symbol']} on {trade_details['date']}", font=font, fill="black")
        draw.text((10, 40), f"Long/Short: {trade_details['long_short']}", font=font, fill="black")
        draw.text((10, 70), f"Margin: {trade_details['margin']}", font=font, fill="black")
        draw.text((10, 100), f"Leverage: {trade_details['leverage']}", font=font, fill="black")
        draw.text((10, 130), f"Open Price: {trade_details['open_price']}", font=font, fill="black")
        draw.text((10, 160), f"Current Price: {trade_details['current_price']}", font=font, fill="black")
        draw.text((10, 190), f"Return PnL: {trade_details['return_pnl']}", font=font, fill="black")

        # Save the image to a BytesIO object
        image_io = BytesIO()
        image.save(image_io, format="PNG")

        return ContentFile(image_io.getvalue(), name="trade_image.png")
    
def search_trade(request):
    # logic to handle trade search
    query = request.GET.get('query', '')
    user_id = request.GET.get('user_id', '')

    try:
        # Attempt to convert the user_id to an integer
        user_id = int(user_id)
    except ValueError:
        # Handle the case where the user_id is not a valid integer
        return JsonResponse([], safe=False)

    # Get the user's trades based on the query
    user_trades = Trade.objects.filter(user_id=user_id, id=query)

    # Prepare the response data
    response_data = []
    for trade in user_trades:
        response_data.append({
            'id': trade.id,
            'user_name': trade.user.username,
            'symbol': trade.symbol,
            'date': trade.date.strftime('%Y-%m-%d'),  # Format the date
            'long_short': trade.long_short,
            'margin': float(trade.margin),
            'leverage': float(trade.leverage),
            'open_price': float(trade.open_price),
            'current_price': float(trade.current_price),
            'return_pnl': float(trade.return_pnl),
        })

    return JsonResponse(response_data, safe=False)

    # Prepare the results as a list of dictionaries
    results = [{'id': trade.id, 'symbol': trade.symbol, 'date': trade.date} for trade in trades_results]

    # Return the results as a JSON response
    return JsonResponse(results, safe=False)


    # Prepare the results as a list of dictionaries
    results = [{'id': trade.id, 'symbol': trade.symbol, 'date': trade.date} for trade in trades_results]

    return JsonResponse(results, safe=False)

def get_trade_details(request):
    trade_id = request.GET.get('trade_id')

    # Perform a database query to get trade details based on trade_id
    try:
        trade = Trade.objects.get(id=trade_id)
        trade_details = {'id': trade.id, 'symbol': trade.symbol, 'date': trade.date}
        return JsonResponse(trade_details)
    except Trade.DoesNotExist:
        return JsonResponse({'error': 'Trade not found'}, status=404)