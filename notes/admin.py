from django.contrib import admin

from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_type', 'owner', 'created_at', 'updated_at')

admin.site.register(Note, NoteAdmin)
