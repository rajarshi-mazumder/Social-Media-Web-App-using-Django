
from email.policy import default
from random import choices
from secrets import choice
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import int_list_validator
from django.contrib.postgres.fields import ArrayField
from datetime import datetime, date
from ckeditor.fields import RichTextField
# from spacy import blank
import json

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    tags = models.CharField(
        max_length=255, default='none')

    def save(self, *args, **kwargs):
        self.tags = self.name.replace(' ', '-').lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home-page')


class Community(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile")
    community_header_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile")
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, default=None)
    members = models.ManyToManyField(
        User, default=None, blank=True, related_name='members')
    is_private = models.BooleanField(null=True, blank=True, default=False)
    community_admins = models.ManyToManyField(
        User, default=None, blank=True, related_name='community_admins')

    post_date = models.DateField(auto_now_add=True)
    post_datetime = models.DateTimeField(auto_now_add=True)

    # post = models.ManyToManyField(
    #     Post, default=None, blank=True, related_name='community_posts')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile")
    discord_link = models.CharField(max_length=255, null=True, blank=True)
    twitch_link = models.CharField(max_length=255, null=True, blank=True)
    following = models.ManyToManyField(
        User, default=None, blank=True, related_name='following')
    followers = models.ManyToManyField(
        User, default=None, blank=True, related_name='followers')
    communities = models.ManyToManyField(
        Community, default=None, blank=True, related_name='communities')
    featured_communities = models.ManyToManyField(
        Community, default=None, blank=True, related_name='featuredCommunities')

    def __str__(self):
        return str(self.user)


empty_list = []


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    body = RichTextField(blank=True, null=True)
    # body = models.TextField()
    reply_to = models.IntegerField(null=True, blank=True, default=-1)
    is_reply = models.BooleanField(null=True, default=False, blank=True)
    is_parent_a_reply = models.BooleanField(
        null=True, default=False, blank=True)
    reply_root = models.IntegerField(null=True, blank=True, default=-1)
    post_date = models.DateField(auto_now_add=True)
    post_datetime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, default='none')
    tags = models.CharField(
        max_length=255, default='', blank=True)
    likes = models.ManyToManyField(
        User, default=None, blank=True, related_name='posts')
    like_count = models.BigIntegerField(default='0')
    reply_count = models.BigIntegerField(default='0')
    video = models.FileField(null=True, blank=True, upload_to="videos/")
    has_images = models.BooleanField(null=True, blank=True, default=False)
    has_video = models.BooleanField(null=True, blank=True, default=False)
    user_profile = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, default=None, null=True, blank=True,)
    body = RichTextField(blank=True, null=True)
    community = models.ForeignKey(
        Community, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    images_ids_list = ArrayField(models.IntegerField(
        null=True, blank=True, default=-1), blank=True, null=True, default=list)
    images_urls_list = ArrayField(models.CharField(
        max_length=500, null=True, blank=True, default=""), blank=True, null=True, default=list)

    def set_Tag(self, lst):
        self.tags = json.dumps(lst)

    def get_Tag(self):
        if self.tags:
            try:

                tag_list = json.loads(self.tags)
                return tag_list
            except ValueError as e:
                return ""

    def liked_by(self):
        likers = []
        for a in self.likes.all():
            likers.append(a.username)
        return likers

        return ', '.join([a.username for a in self.likes.all()])
        return self.likes.all()

    @property
    def num_likes(self):
        return self.likes.all().count()

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        # self.tags = self.category.replace(' ', '-').lower()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.body + ' | ' + str(self.author) + '| ' + str(self.id) + ' | ' + str(self.is_reply)

    def get_absolute_url(self):
        return reverse('post-page', args=(str(self.post_id)))


class Tags(models.Model):
    tag_name = models.CharField(max_length=50, null=True)
    post = models.ManyToManyField(
        Post, default=None, blank=True, related_name='tagged_posts')

    def __str__(self):
        return self.tag_name


class Replies(models.Model):
    reply_to_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    reply_to = models.IntegerField(null=True, blank=True, default=-1)
    post_id = models.IntegerField(null=True, blank=True, default=-1)
    reply_root = models.IntegerField(null=True, blank=True, default=-1)

    def __str__(self):
        return 'Reply to: ' + str(self.reply_to) + ' | ' + 'Post id: ' + str(self.post_id) + ' | ' + 'reply root: ' + str(self.reply_root)


class ImageFiles(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='images/')


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class GameProfile(models.Model):
    games_list = [('Valorant', 'Valorant'), ('Call of Duty', 'Call of Duty'),
                  ('League of Legends', 'League of Legends'), ('Counter Shit: GO', 'Counter Shit: GO')]

    class ValorantServers(models.TextChoices):
        APAC = 'APAC', 'Asia Pacific'
        EMEA = 'EMEA', 'Europe'
        NA = 'NA', 'North America(meaning shit)'
        JA = 'JA', 'Japan'

    class CODServers(models.TextChoices):
        APAC = 'APAC', 'Asia Pacific'
        EMEA = 'EMEA', 'Europe'
        NA = 'NA', 'North America(meaning shit)'

    class LOLServers(models.TextChoices):
        APAC = 'APAC', 'Asia Pacific'
        EMEA = 'EMEA', 'Europe'
        NA = 'NA', 'North America(meaning shit)'

    class CSServers(models.TextChoices):
        EMEA = 'EMEA', 'Europe'
        NA = 'NA', 'North America(meaning shit)'

    class ValorantRanks(models.TextChoices):
        Iron = 'IRON', 'Iron :((('
        Bronze = 'Bronze', 'Bronze :(('
        Silver = 'Silver', 'Silver :('
        Gold = 'Gold', 'Gold :('
        Platinum = 'Platinum', 'Platinum '
        Diamond = 'Diamond', 'Diamond :) '
        Asencdant = 'Asencdant', 'Asencdant :)) '
        Immortal = 'Immortal', 'Immortal >_< '
        Radiant = 'Radiant', 'Radiant :> '

    class LOLRanks(models.TextChoices):
        Iron = 'IRON', 'Iron :((('
        Bronze = 'Bronze', 'Bronze :(('
        Silver = 'Silver', 'Silver :('
        Gold = 'Gold', 'Gold :('
        Platinum = 'Platinum', 'Platinum '
        Diamond = 'Diamond', 'Diamond :) '
        Master = 'Master', 'Master :)) '
        Grandmaster = 'Grandmaster', 'Grandmaster >_< '
        Challenger = 'Challenger', 'Challenger :> '

    class CODRanks(models.TextChoices):
        Rookie = 'Rookie', 'Rookie :((('
        Veteran = 'Veteran', 'Veteran :(('
        Elite = 'Elite', 'Elite :('
        Pro = 'Pro', 'Pro :('
        Master = 'Master', 'Master '
        Grandmaster = 'Grandmaster', 'Grandmaster :) '
        Legendary = 'Legendary', 'Legendary :)) '

    class CSRanks(models.TextChoices):

        Silver = 'Silver', 'Silver :('
        Gold = 'Gold', 'Gold :('
        Master_Guardian = 'Master Guardian', 'Master Guardian '
        Distinguished_Master_Guardian = 'Distinguished Master Guardian', 'Distinguished Master Guardian :) '
        Legendary = 'Legendary', 'Legendary :)) '
        Elite = 'Elite', 'Elite >_< '

    class User_Status(models.TextChoices):
        LFTeams = 'Looking for teams', 'Looking for teams'
        LFTalent = 'Looking for talent', 'Looking for talent'
        none = 'none', 'none'

    servers_list = [('Val', ValorantServers.choices), ('COD', CODServers.choices),
                    ('LOL', LOLServers.choices), ('CS', CSServers.choices)]

    ranks_list = [('Val', ValorantRanks.choices), ('COD', CODRanks.choices),
                  ('LOL', LOLRanks.choices), ('CS', CSRanks.choices)]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    game = models.CharField(max_length=50, choices=games_list)
    server = models.CharField(max_length=50, choices=servers_list)
    rank = models.CharField(max_length=50, choices=ranks_list, default="")
    user_status = models.CharField(
        max_length=50, choices=User_Status.choices, default='none')

    def __str__(self):
        return str(self.user) + " | " + str(self.game) + " | " + str(self.server) + " | " + str(self.rank)
