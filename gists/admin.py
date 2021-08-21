from django.contrib import admin
from .models import Gist, Owner, GistFile

admin.site.register(Gist)
admin.site.register(Owner)
admin.site.register(GistFile)
