from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.generic import ListView, DetailView, UpdateView
from matplotlib.style import context
from . models import Community, GameProfile, Post, Replies, ImageFiles, Profile, Tags, Main_Profile
from . forms import EditPostForm, EditVideoPostForm, ImageForm, PostForm, PostImageForm, PostVideoForm, EditImagePostForm, GameProfileForm, MatchmakingForm, CreateCommunityForm, EditCommunityForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
from django.conf.urls.static import static
# Create your views here.
# Paginator stuff
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .serializers import PostSerializer
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


def get_featured_communities(request):
    communities = Community.objects.all()[:5]
    joined_communities = ""
    try:
        joined_communities = request.user.profile.communities.all()
    except:
        joined_communities = ""

    return communities, joined_communities


def Get_Gamer_Profiles_For_User_profiles_Page(request, user):
    desired_gamer_profiles = GameProfile.objects.filter(user=user)
    gamer_profiles = GameProfile.objects.filter(user=request.user)

    try:
        desired_main_gamer_profile = Main_Profile.objects.get(
            user=User.objects.get(username=user))
        main_gamer_profile = Main_Profile.objects.get(
            user=User.objects.get(username=request.user))
    except:
        if Main_Profile.objects.filter(
                user=User.objects.get(username=user)).exists():
            desired_main_gamer_profile = None
            main_gamer_profile = None

        else:
            desired_main_gamer_profile = None
            main_gamer_profile = Main_Profile.objects.get(
                user=User.objects.get(username=request.user))

    print("Lautaro", Main_Profile.objects.get(
        user=User.objects.get(username=request.user)), " Martizez ", main_gamer_profile)

    context = {'desired_gamer_profiles': desired_gamer_profiles,
               'gamer_profiles': gamer_profiles,
               'desired_main_gamer_profile': desired_main_gamer_profile,
               'main_game_profile': main_gamer_profile}

    return context
