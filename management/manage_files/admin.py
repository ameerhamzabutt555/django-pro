from django.contrib import admin
from .models import ManagedFile
from django.urls import reverse
from django.utils.html import format_html
from urllib.parse import quote



# Register your models here.



def update_files(modeladmin, request, queryset):
    for item in queryset:
        # Implement your file updating logic here
        pass

update_files.short_description = "Update selected files"

class ManagedFileAdmin(admin.ModelAdmin):
    actions = [update_files]

    list_display = ["name", "file", "file_link"]

    def file_link(self, obj):
        if obj.file:
            file_url = obj.file.url
            print("obj.file.url", obj.file.url)
            return format_html('<a href="{}">Download</a>', file_url)
        return None

    file_link.short_description = 'Download File'


admin.site.register(ManagedFile, ManagedFileAdmin)
