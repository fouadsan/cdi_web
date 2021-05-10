from django.contrib import admin
from .models import Banner, Section, Teammate


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'alt_text')  # , 'image_tag'


admin.site.register(Banner, BannerAdmin)
admin.site.register(Section)
admin.site.register(Teammate)
