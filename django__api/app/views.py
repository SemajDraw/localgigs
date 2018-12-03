from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfilePicForm, ProfileForm


# Render landing page
def landing(request):
    return render(request, 'app/landing.html')


# Render profile page
@login_required
def profile(request):
    return render(request, 'app/profile.html')


# Accepts a post request from a ProfileForm that is used to update the profile
# associated to the authenticated user.
@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_details = ProfileForm(request.POST, instance=request.user.profile)
        if profile_details.is_valid():
            profile_details.save()
            return render(request, 'app/profile.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm()
    return render(request, 'app/update_profile_details.html', {
        'profile_form': form
    })


# Accepts a post request from a ProfilePic Form that is used to update the profile
# picture associated to the authenticated user.
@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_pic_form.is_valid():
            profile_pic_form.save()
            return render(request, 'app/profile.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfilePicForm()
    return render(request, 'app/update_profile_pic.html', {
        'profile_pic_form': form
    })


