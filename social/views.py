# social/views.py
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Group
from .forms import GroupCreationForm, GroupSearchForm
from user.models import UserProfile
from django.contrib.auth.decorators import login_required




# @login_required
# def create_group(request):
#     group_id = None

#     if request.method == 'POST':
#         form = GroupCreationForm(request.POST)
#         if form.is_valid():
#             group = form.save(commit=False)
#             group.creator = request.user
#             group.save()
#             group.members.add(request.user)
#             # Get the group_id after saving the form
#             group_id = group.group_id

#             # Redirect to the 'group_detail' view with the correct group_id
#             return redirect('social:group_detail', group_id=group_id)

#     else:
#         form = GroupCreationForm()
#     return render(request, 'create_group.html', {'form': form, 'group_id': group_id})


from django.shortcuts import render, redirect
from .models import Group
from .forms import GroupCreationForm
from django.contrib.auth.decorators import login_required

# social/views.py
from django.shortcuts import render, redirect
from .models import Group
from .forms import GroupCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def create_group(request):
    group_id = None

    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            # Save tags
            tags = form.cleaned_data.get('tags')
            if tags:
                # Split tags by comma and strip whitespace
                tag_list = [tag.strip() for tag in tags.split(',')]
                # Add tags to the group
                group.tags = ','.join(tag_list)
                group.save()

            # Get the group_id after saving the form
            group_id = group.group_id
            # Redirect to the 'group_detail' view with the correct group_id
            return redirect('social:group_detail', group_id=group_id)

    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {'form': form, 'group_id': group_id})



@login_required
def search_group(request):
    user_groups = []

    if request.user.is_authenticated:
        user_groups = request.user.group_members.all()

    search_results = []

    if request.method == 'POST':
        form = GroupSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']

            groups = Group.objects.filter(group_id__exact=search_query)

            for group in groups:
                already_member = group in user_groups
                search_results.append((group, already_member))
    else:
        form = GroupSearchForm()

    return render(request, 'search_group.html', {'form': form, 'search_results': search_results, 'user_groups': user_groups})

@login_required
def join_group(request, group_id):
    group = Group.objects.get(group_id=group_id)
    group.members.add(request.user)
    return redirect('social:group_detail', group_id=group.group_id)


# social/views.py

@login_required
def group_detail(request, group_id):
    group = Group.objects.get(group_id=group_id)
    user_groups = request.user.group_members.all()

    # Use reverse with the app name and URL pattern name
    group_detail_url = reverse('social:group_detail', args=[group_id])

    return render(request, 'group_detail.html', {'group': group, 'user_groups': user_groups, 'group_detail_url': group_detail_url})


from .models import Group

# def feeds_view(request):
#     # Retrieve the user's profile
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         user_profile = None

#     # Retrieve the user's groups
#     user_groups = Group.objects.filter(members=request.user)

#     return render(request, 'feeds.html', {'user': request.user, 'user_profile': user_profile, 'user_groups': user_groups})

# social/views.py

from django.shortcuts import render
from .models import Post
from user.models import UserProfile
@login_required
def feeds_view(request):
    # Retrieve the user's profile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    # Retrieve the user's groups
    user_groups = Group.objects.filter(members=request.user)

    # Retrieve all posts of the current user
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'feeds.html', {'user': request.user, 'user_profile': user_profile, 'user_posts': user_posts, 'user_groups': user_groups})






from django.shortcuts import render, redirect
from .forms import GroupCreationForm, GroupSearchForm, GroupJoinForm, PostCreationForm
from .models import Group, Post
from user.models import UserProfile

from django.contrib import messages


# from .forms import PostCreationForm


# def create_post(request):
#     if request.method == 'POST':
#         post_form = PostCreationForm(request.user, request.POST, request.FILES)
#         if post_form.is_valid():
#             post = post_form.save(commit=False)
#             post.user = request.user
#             post.save()

#             messages.success(request, 'Post successfully created!')
#             return redirect('social:feeds')
#     else:
#         post_form = PostCreationForm(user=request.user)  # Pass the user to the form

#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         user_profile = None

#     user_groups = Group.objects.filter(members=request.user)
#     user_posts = Post.objects.filter(user__in=user_groups.values_list('members', flat=True)).order_by('-created_at')

#     return render(request, 'feeds.html', {'user': request.user, 'user_profile': user_profile, 'user_groups': user_groups, 'user_posts': user_posts, 'post_form': post_form})

from django.shortcuts import render, redirect
from .forms import PostCreationForm
from .models import Post
from django.contrib import messages
from user.models import UserProfile
from .models import Group  

from django.shortcuts import render, redirect
from .forms import PostCreationForm
from .models import Post
from django.contrib import messages
from user.models import UserProfile
from .models import Group 
 
@login_required
def create_post(request):
    user_groups = Group.objects.filter(members=request.user)

    if request.method == 'POST':
        post_form = PostCreationForm(request.user, request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post.groups.set(post_form.cleaned_data['groups'])

            # Debugging: Print post information
            print(f"Post created - ID: {post.id}, Caption: {post.caption}, User: {post.user.username}")

            # Print associated groups
            print("Associated Groups:")
            for group in post.groups.all():
                print(f"- {group.name}")

            messages.success(request, 'Post successfully created!')

            # Redirect to the feeds page
            return redirect('social:feeds_view')

    post_form = PostCreationForm(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user) if UserProfile.objects.filter(user=request.user).exists() else None

    # Retrieve the user's posts
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    # Debugging: Print user posts
    print("User Posts:")
    for user_post in user_posts:
        print(f"- {user_post.id} - {user_post.caption}")

    return render(request, 'feeds.html', {'user': request.user, 'user_profile': user_profile, 'user_groups': user_groups, 'user_posts': user_posts, 'post_form': post_form})

