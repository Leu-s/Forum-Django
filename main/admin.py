from django.contrib import admin
from .models import AdvancedUser
from.models import VillagesOfBershad
from .models import Article, Category

admin.site.register(AdvancedUser)
admin.site.register(VillagesOfBershad)
admin.site.register(Article)
admin.site.register(Category)
