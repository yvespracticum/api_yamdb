from django.contrib import admin

from .models import User
from reviews.models import Review, Comment, Title

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
