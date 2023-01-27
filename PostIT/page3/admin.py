
from django.contrib import admin
from . models import Post, Category, Profile, Replies, ImageFiles, GameProfile, Tags, Community

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Replies)
admin.site.register(ImageFiles)
admin.site.register(GameProfile)
admin.site.register(Tags)
admin.site.register(Community)
