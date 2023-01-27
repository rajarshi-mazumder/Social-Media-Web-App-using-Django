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
    featured_communities = Community.objects.all()[:5]
    joined_communities = ""
    try:
        joined_communities = request.user.profile.communities.all()
    except:
        joined_communities = ""
    context = {
        'featured_communities': featured_communities,
        'joined_communities': joined_communities,
    }
    return context


def Get_Gamer_Profiles_For_User_profiles_Page(request, user):

    try:
        selected_user_gamer_profiles = GameProfile.objects.filter(user=user)
        selected_user_main_gamer_profile = Main_Profile.objects.get(
            user=User.objects.get(username=user))

    except:
        selected_user_gamer_profiles = None
        selected_user_main_gamer_profile = None

    context = {'selected_user_gamer_profiles': selected_user_gamer_profiles,
               'selected_user_main_gamer_profile': selected_user_main_gamer_profile,
               'game_logos': GameProfile.games_logo_list, }
    print("Aimer: ", context)

    return context


def Get_Logged_in_User_Gamer_Profiles(request, user):
    try:
        gamer_profiles = GameProfile.objects.filter(user=request.user)
        main_gamer_profile = Main_Profile.objects.get(
            user=User.objects.get(username=request.user))
    except:
        gamer_profiles = None
        main_gamer_profile = None

    context = {'gamer_profiles': gamer_profiles,
               'main_game_profile': main_gamer_profile, }

    return context


def get_gamer_profile_info_sidebar(request):
    try:
        gamer_profiles = GameProfile.objects.filter(user=request.user)
        main_gamer_profile = Main_Profile.objects.get(
            user=User.objects.get(username=request.user))
    except:
        gamer_profiles = None
        main_gamer_profile = None

    context = {'gamer_profiles': gamer_profiles,
               'main_game_profile': main_gamer_profile,
               'game_logos': GameProfile.games_logo_list, }

    return context


@login_required
@csrf_exempt
def get_user_vouch_information(request, user):
    try:
        if user.profile.vouched_by.filter(id=request.user.id).exists():
            vouched_for_user = True
        else:
            vouched_for_user = False

        context = {
            'vouch_count': user.profile.vouched_by.count(),
            'vouched_for_user': vouched_for_user,
        }
    except:
        context = {}
    return context


@login_required
@csrf_exempt
def get_user_following_info(request):
    users_currently_following = request.user.profile.following.all()
    context = {
        'users_currently_following': users_currently_following,
    }
    return context


@login_required(login_url='/users/login_user')
@csrf_exempt
def get_user_gamer_profile_data(request, game):

    gamer_profiles = GameProfile.objects.filter(
        user=User.objects.get(username=request.user), game=game)

    # main_gamer_profile = Main_Profile.objects.get(
    #     user=User.objects.get(username=request.user))
    # additional_info = []
    # for g in gamer_profiles:
    #     info_obj = g.additional_info

    #     dict_obj = {}
    #     for i in range(len(info_obj)):
    #         dict_obj[i] = info_obj[i]
    #     additional_info.append({'game': g.game,
    #                             'info': dict_obj})

    context = {
        'selected_gamer_profiles': gamer_profiles,
        # 'main_gamer_profile': main_gamer_profile,
        # 'additional_info': additional_info,
        # 'game_logos': GameProfile.games_logo_list,
    }
    return gamer_profiles
    html = render_to_string(
        'gamerProfile/gamer_profile_stats.html', context, request=request)
    print(context)
    return JsonResponse({"gamer_profile_stats": html,
                         'game_logo': GameProfile.games_logo_list[gamer_profiles[0].game],
                         })
