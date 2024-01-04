from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import BlogPost, Trade
from .forms import BlogPostForm
from PIL import Image, ImageDraw, ImageFont
import base64
from django.core.files.base import ContentFile
from io import BytesIO

class BlogView(View):
    blog = 'blog.html'

    def get(self, request, *args, **kwargs):
        blog_post_form = BlogPostForm()
        posts = BlogPost.objects.all()

        # Split all posts into three sets for three boxes
        num_boxes = 3
        posts_sets = [posts[i::num_boxes] for i in range(num_boxes)]

        context = {'blog_post_form': blog_post_form, 'posts_sets': posts_sets}

        if request.user.is_authenticated:
            user_name = request.user.username 
            context['user_name'] = user_name

        return render(request, self.blog, context)

    def post(self, request, *args, **kwargs):
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        print('post', request.POST)
        print('files', request.FILES)

        print("POST request received.")
        
        if blog_post_form.is_valid():
            new_post = blog_post_form.save(commit=False)
            new_post.user = request.user

            # Validate required fields
            if not new_post.title or not new_post.content:
                # Handle form validation errors
                errors = blog_post_form.errors
                print(f"Form validation errors: {errors}")
                return JsonResponse({'error': 'Form validation failed', 'errors': errors})

            # If trade_image is present, process it
            trade_image = request.FILES.get('trade_image')

            # Save the new post
            new_post.save()
            print(f"Post saved successfully: {new_post.title}")

            return JsonResponse({'success': True, 'message': 'Post and image uploaded successfully'})

        # If form is not valid
        errors = blog_post_form.errors
        print(f"Form validation errors: {errors}")
        return JsonResponse({'error': 'Form validation failed', 'errors': errors})
    
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
        print(f"User ID: {user_id}")
    except ValueError:
        # Handle the case where the user_id is not a valid integer
        print("Invalid user ID. Could not convert to integer.")
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
    print(f"Results: {results}")
    return JsonResponse(results, safe=False)


    # Prepare the results as a list of dictionaries
    results = [{'id': trade.id, 'symbol': trade.symbol, 'date': trade.date} for trade in trades_results]

    # Return the results as a JSON response
    print(f"Results: {results}")
    return JsonResponse(results, safe=False)

def get_trade_details(request):
    trade_id = request.GET.get('trade_id')

    print(f"Searching for trade details with trade_id: {trade_id}")

    # Perform a database query to get trade details based on trade_id
    try:
        trade = Trade.objects.get(id=trade_id)
        trade_details = {'id': trade.id, 'symbol': trade.symbol, 'date': trade.date}
        print(f"Trade details found: {trade_details}")
        return JsonResponse(trade_details)
    except Trade.DoesNotExist:
        print("Trade not found.")
        return JsonResponse({'error': 'Trade not found'}, status=404)

