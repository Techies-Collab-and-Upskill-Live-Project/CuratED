from django.contrib import admin
from .models import Playlist, PlaylistItem

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 1 # Number of empty forms to display
    ordering = ('order',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'item_count')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'description', 'user__email')
    inlines = [PlaylistItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'playlist', 'video_id', 'order', 'added_at')
    list_filter = ('playlist__user', 'playlist__name', 'added_at')
    search_fields = ('title', 'video_id', 'playlist__name')
    ordering = ('playlist', 'order')
