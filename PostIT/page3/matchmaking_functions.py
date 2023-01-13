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


def Filter_Profiles(request):
    print(request.POST)
    pref_game = request.POST['game']
    pref_region = request.POST['region']
    rank = request.POST['rank']
    pref_servers = request.POST.getlist('servers[]')
    matched_profiles = []
    proflies = []
    print("pref_servers", pref_servers, " Metropolitano")
    game_profiles = GameProfile.objects.filter(
        game__contains=pref_game, region__contains=pref_region)

    rank_order = 0
    searched_rank = ""
    next_rank = ""
    prev_rank = ""

    if(pref_game == "Valorant"):
        rank_order = GameProfile.Valorant_Ranks_Order[rank]
        searched_rank = rank
        if(rank_order == 1):
            prev_rank = searched_rank
            next_rank = [
                k for k, v in GameProfile.Valorant_Ranks_Order.items() if v == rank_order+1][0]

        elif rank_order == GameProfile.Valorant_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.Valorant_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = searched_rank
        elif rank_order > 1 and rank_order < GameProfile.Valorant_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.Valorant_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = [
                k for k, v in GameProfile.Valorant_Ranks_Order.items() if v == rank_order+1][0]

    elif(pref_game == "Call of Duty"):
        rank_order = GameProfile.COD_Ranks_Order[rank]
        searched_rank = rank
        if(rank_order == 1):
            prev_rank = searched_rank
            next_rank = [
                k for k, v in GameProfile.COD_Ranks_Order.items() if v == rank_order+1][0]

        elif rank_order == GameProfile.COD_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.COD_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = searched_rank
        elif rank_order > 1 and rank_order < GameProfile.COD_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.COD_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = [
                k for k, v in GameProfile.COD_Ranks_Order.items() if v == rank_order+1][0]

    elif(pref_game == "League of Legends"):
        rank_order = GameProfile.LOL_Ranks_Order[rank]
        searched_rank = rank
        if(rank_order == 1):
            prev_rank = searched_rank
            next_rank = [
                k for k, v in GameProfile.LOL_Ranks_Order.items() if v == rank_order+1][0]

        elif rank_order == GameProfile.LOL_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.LOL_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = searched_rank
        elif rank_order > 1 and rank_order < GameProfile.LOL_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.LOL_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = [
                k for k, v in GameProfile.LOL_Ranks_Order.items() if v == rank_order+1][0]

    elif(pref_game == "Counter Strike: GO"):
        rank_order = GameProfile.CS_Ranks_Order[rank]
        searched_rank = rank
        if(rank_order == 1):
            prev_rank = searched_rank
            next_rank = [
                k for k, v in GameProfile.CS_Ranks_Order.items() if v == rank_order+1][0]

        elif rank_order == GameProfile.CS_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.CS_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = searched_rank
        elif rank_order > 1 and rank_order < GameProfile.CS_Ranks_Order["Max_Rank"]:
            prev_rank = [
                k for k, v in GameProfile.CS_Ranks_Order.items() if v == rank_order-1][0]
            next_rank = [
                k for k, v in GameProfile.CS_Ranks_Order.items() if v == rank_order+1][0]

    for g in game_profiles:

        queried_user = User.objects.get(username=g.user).id
        quieried_user_profile = User.objects.get(username=g.user)
        queried_profile = (Profile.objects.filter(user=int(queried_user)))

        servers_present = False
        for user_server in g.servers:

            for queried_server in pref_servers:
                if queried_server == user_server:
                    servers_present = True

        if(g.rank == rank and servers_present):
            if(queried_profile):
                print(queried_profile[0].bio)
                obj = {'username': g.user.username, 'game': g.game, 'rank': g.rank, 'region': g.region,
                       'bio': queried_profile[0].bio, 'profile_pic': str(queried_profile[0].profile_pic), 'user_status': g.user_status}
                proflies.append(obj)
                matched_profiles.append(quieried_user_profile)

        print("Nightmare :", rank_order)
        print("prev_rank :", prev_rank)
        print("searched_rank :", searched_rank)
        print("next_rank :", next_rank)

        for g in game_profiles:
            queried_user = User.objects.get(username=g.user).id
            quieried_user_profile = User.objects.get(username=g.user)
            queried_profile = (Profile.objects.filter(user=int(queried_user)))
            queried_game = pref_game
            max_rank_number = 0
            high_elo_check = False

            if(queried_game == "Valorant"):
                max_rank_number = GameProfile.Valorant_Ranks_Order["Max_Rank"]

                if rank_order >= max_rank_number-2:
                    high_elo_ranks = [
                        k for k, v in GameProfile.Valorant_Ranks_Order.items() if v >= max_rank_number-2]
                    for r in high_elo_ranks:
                        if g.rank == r:
                            high_elo_check = True

            elif(queried_game == "Call of Duty"):
                max_rank_number = GameProfile.COD_Ranks_Order["Max_Rank"]

                if rank_order >= max_rank_number-2:
                    high_elo_ranks = [
                        k for k, v in GameProfile.COD_Ranks_Order.items() if v >= max_rank_number-2]
                    for r in high_elo_ranks:
                        if g.rank == r:
                            high_elo_check = True

            elif(queried_game == "League of Legends"):
                max_rank_number = GameProfile.LOL_Ranks_Order["Max_Rank"]

                if rank_order >= max_rank_number-2:
                    high_elo_ranks = [
                        k for k, v in GameProfile.LOL_Ranks_Order.items() if v >= max_rank_number-2]
                    for r in high_elo_ranks:
                        if g.rank == r:
                            high_elo_check = True
            elif(queried_game == "Counter Strike: GO'"):
                max_rank_number = GameProfile.CS_Ranks_Order["Max_Rank"]
                if rank_order >= max_rank_number-2:
                    high_elo_ranks = [
                        k for k, v in GameProfile.CS_Ranks_Order.items() if v >= max_rank_number-2]
                    for r in high_elo_ranks:
                        if g.rank == r:
                            high_elo_check = True

            servers_present = False
            for user_server in g.servers:

                for queried_server in pref_servers:
                    if queried_server == user_server:
                        servers_present = True

            if servers_present and ((prev_rank != searched_rank and g.rank == prev_rank) or (next_rank != searched_rank and g.rank == next_rank) or (high_elo_check and g.rank != searched_rank)):
                if(queried_profile):
                    print(queried_profile[0].bio)
                    obj = {'username': g.user.username, 'game': g.game, 'rank': g.rank, 'region': g.region,
                           'bio': queried_profile[0].bio, 'profile_pic': str(queried_profile[0].profile_pic), 'user_status': g.user_status}
                    proflies.append(obj)
                    matched_profiles.append(quieried_user_profile)

        return matched_profiles
