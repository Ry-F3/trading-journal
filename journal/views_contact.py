# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from .forms import FAQForm, AdminResponseForm
from .models import FAQRequest
from django.utils import timezone
from django.contrib import messages

class ContactUsView(View):
    contact = 'contact.html'

    @staticmethod
    def initialize_faq_context():
        faqs_per_box = 1
        faq_sets = {}
        updated_remaining_faqs = []

        # Fetch all FAQs once
        all_faqs = FAQRequest.objects.all()

        # Order all FAQs by timestamp
        all_faqs_ordered = sorted(all_faqs, key=lambda faq: faq.timestamp, reverse=True)

        # Divide FAQs into sets
        faqs_sets = [all_faqs_ordered[i:i + faqs_per_box] for i in range(0, len(all_faqs_ordered), faqs_per_box)]

        # Fill up faq sets with empty lists if necessary
        for _ in range(3 - len(faqs_sets)):
            faqs_sets.append([])

        # Split FAQs into faq sets and remaining FAQs
        remaining_faqs = all_faqs_ordered[len(faqs_sets) * faqs_per_box:]

        # Order remaining FAQs by timestamp
        remaining_faqs = sorted(remaining_faqs, key=lambda faq: faq.timestamp, reverse=True)

        # Order each faq set by timestamp
        faqs_sets = [sorted(faqs_set, key=lambda faq: faq.timestamp, reverse=False) for faqs_set in faqs_sets]

        # Exclude faqs in faq_sets from remaining_faqs using list comprehension
        remaining_faqs = [faq for faq in remaining_faqs if faq not in [item for sublist in faqs_sets for item in sublist]]

        # Create a new list with actual objects to preserve previous FAQs and append the fourth FAQ
        updated_remaining_faqs = list(remaining_faqs)

        # Append all FAQs starting from the fourth one to updated_remaining_faqs
        remainder_index = 3
        updated_remaining_faqs += all_faqs_ordered[remainder_index:] if len(all_faqs_ordered) > remainder_index else []
              
        # Return the initialised context
        return {
            'faqs_sets': faqs_sets,
            'updated_remaining_faqs': updated_remaining_faqs,
        }

    def get(self, request, *args, **kwargs):
        context = self.initialize_faq_context()
        if request.user.is_authenticated:
            user_name = request.user.username
            context['user_name'] = user_name
        return render(request, self.contact, context)

    def post(self, request, *args, **kwargs):
        # Handle the form data here
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Create and save a new FAQRequest instance
        new_faq = FAQRequest.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            title=title,
            question=content,
            is_approved=False 
        )

        # Fetch the updated FAQs for rendering
        context = self.initialize_faq_context()

        # Redirect to the same page to avoid form resubmission on page reload
        return redirect(reverse('contact'))  


@login_required
def submit_faq_request(request):
    context = {}  # Initialise an empty context
    messages.success(request, 'FAQ request sent!')
    if request.method == 'POST':
        # Handle the form data here
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Create and save a new FAQRequest instance
        new_faq = FAQRequest.objects.create(
            user=request.user,
            timestamp=timezone.now(),
            title=title,
            question=content,
            is_approved=False
        )

        # Fetch the updated FAQs for rendering
        context.update(ContactUsView().initialize_faq_context())

        # Redirect to the same page to avoid form resubmission on page reload
        return redirect(reverse('contact')) 

    # If not a POST request, you can handle it accordingly
    return JsonResponse({'message': 'Invalid request method'})

def faq_list(request):
    # Get all approved FAQRequest objects with their AdminResponse
    faqs_with_responses = FAQRequest.objects.filter(is_approved=True, adminresponse__is_sent=True).order_by('-timestamp')

    context = {'faqs_with_responses': faqs_with_responses}
    return render(request, 'contact.html', context)


def view_faq(request, faq_id):
    # Get the specific FAQ based on faq_id
    faq = get_object_or_404(FAQRequest, id=faq_id)

    # Fetch the updated FAQs for rendering the FAQ section
    context = ContactUsView().initialize_faq_context()

    # Add the specific FAQ to the context
    context['faq'] = faq

    # Render the HTML with the updated FAQs and the specific FAQ
    return render(request, 'contact.html', context)

