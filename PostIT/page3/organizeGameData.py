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


def organizeGametData(request, profileData):
    profile_info = ""
    print("hkuefhuk")
    for data in profileData:
        print("klklkl", data)
        if data.game == "Valorant":

            if not(data.user_status == "none"):
                profile_info += "-"+data.user_status + "\n"

            if (data.in_game_user_id):
                profile_info += "-VALORANT Id: " + data.in_game_user_id + "\n"

            if (data.region):
                profile_info += "-Region: " + data.region + "\n"
            if (data.rank):
                profile_info += "-Current/ Peak Rank: " + \
                    data.rank
            if (data.peak_rank or not data.peak_rank == ""):
                profile_info += "/ " + data.peak_rank + "\n"
            else:
                profile_info += "\n"

            try:
                if (data.experience):
                    exp_info = ""
                    for i in range(len(data.experience)):
                        for j in range(len(data.experience[i])):
                            exp_info += data.experience[i][j]+"-"
                        exp_info += "\n"
                    profile_info += "-Experience: \n"+exp_info + "\n"
                if data.achievements:
                    profile_info += "-"+data.achievements + "\n"
                roles_info = {}
                roles_in_profile_info = ""
            except:
                profile_info = profile_info

            for i in range(len(GameProfile.Valorant_Roles)):
                if data.roles_rating[i] >= 3:
                    roles_info.update(
                        {GameProfile.Valorant_Roles[i]: data.roles_rating[i]})
                    roles_in_profile_info += GameProfile.Valorant_Roles[i]+","

            if not roles_in_profile_info == "":
                profile_info += "-Roles: "+roles_in_profile_info+"\n"
            if data.remarks:
                profile_info += data.remarks + "\n"

            if data.time_available:
                profile_info += "-Time Available: " + data.time_available

            profile_info = "\n" + profile_info

    return profile_info
