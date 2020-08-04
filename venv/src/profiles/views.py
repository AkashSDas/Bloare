from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserUpdateForm


# ****** Profile View ******
# This is a profile of specific user which is visible from there
# accounts only.
""" 
    NOTE: This profile is different from individual User's Profile.
    
    1) User's Profile:
    - User's Profile is visible from that user's account only.
    - User can update there profile data from their User's Profile.
 
    2) Author's Profile:
    - Author's Profile is visible to all other users.
"""


@login_required
def profile_view(request):
    if request.method == 'POST':

        # Inside UserUpdateForm we are passing request.POST that is the data that is
        # changed and the instance parameter is the user that is logged in and want to
        # update information.
        user_update_form = UserUpdateForm(request.POST, instance=request.user)

        # request.FILES - with profile form we will be getting additional data this is
        # going to be file data that is images that user is wants/going to change.
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': user_update_form, 'p_form': profile_update_form}
    return render(request, 'profiles/profile.html', context)
