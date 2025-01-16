from django.http import HttpResponse
from django.shortcuts import render,redirect
from tweets.models import User
from tweets.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def tweet_view(request):
    session = request.session.get('user')
    if not session:
        return redirect('login')
    else:
        user = User.objects.get(email=session)
        return render(request, 'tweet.html',{'user': user})


def profile_view(request):
    session = request.session.get('user')
    if not session:
        return redirect('login')
    else:
        user = User.objects.get(email=session)
        return render(request, 'profile.html', {'user': user})



def edit_profile_view(request):
    # Retrieve user session
    session = request.session.get('user')
    if not session:
        return redirect('login')  # Redirect to login page if session is missing

    try:
        user = User.objects.get(email=session)  # Fetch user by email in session
    except User.DoesNotExist:
        return redirect('login')  # Redirect to login if user is not found

    if request.method == "POST":
        # Bind POST data and FILES to the form instance
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user instance
            return render(request, 'editProfile.html', {
                'form': form,
                'user': user,
                'message': 'Profile updated successfully.',
            })
        else:
            # Handle form validation errors
            return render(request, 'editProfile.html', {
                'form': form,
                'user': user,
                'error': 'Please correct the errors below.',
            })

    # Prepopulate the form with the user's current data for GET requests
    form = ProfileForm(instance=user)
    return render(request, 'editProfile.html', {
        'form': form,
        'user': user,
    })