from django.http import HttpResponse
from django.shortcuts import render,redirect
from tweets.models import User,SkillPost
from tweets.forms import ProfileForm,SkillPostForm
from django.contrib.auth.decorators import login_required
from datetime import datetime



def profile_view(request):
    session = request.session.get('user')
    if not session:
        return redirect('login')
    else:
        user = User.objects.get(email=session)
        post = SkillPost.objects.filter(post_owner=user)
        return render(request, 'profile.html', {'user': user,'skill':post})



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




# View for displaying all posts
def tweet_view(request):
    session = request.session.get('user')
    if not session:
        return redirect('login')
    else:
        user = User.objects.get(email=session)
        skill = SkillPost.objects.all()
        return render(request, 'skill.html', {'user': user, 'skill': skill})



# View for making a new post
def create_new_post(request):
    try:
        session = request.session.get('user')
        if not session:
            return redirect('login')
        else:
            user = User.objects.get(email=session)
            if request.method == "POST":
                post_form = SkillPostForm(request.POST,request.FILES)

                if post_form.is_valid():

                    skill_post = post_form.save(commit=False)
                    skill_post.post_owner = user
                    skill_post.save()

                    return render(request,'skillPost.html',{'post_form':post_form,'message':'Post created successfully'})
                else:
                    return render(request,'skillPost.html',{'post_form':post_form,'error':'Please correct the errors below'})
            else:
                post_form = SkillPostForm()
                return render(request,'skillPost.html',{'post_form':post_form,'user':user})
    except User.DoesNotExist:
        return redirect('login')

