from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Critic)