from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from .models import Links, Skills, Contact
from ckeditor.widgets import CKEditorWidget

class LinksAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "url", "icon")
    list_display_links = ("id", "name")
    search_fields = ("name", "title")
    ordering = ("id",)
    list_per_page = 12
    
class SkillsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    
    list_display = ("id", "name", "display_icon")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)
    list_per_page = 12
    
    def display_icon(self, obj):
        return mark_safe(f'<div style="max-width: 30px; max-height: 30px; overflow: hidden;">{obj.icon}</div>')

class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "subject", "status", "created_at")
    list_display_links = ("id", "full_name")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "subject")
    ordering = ("-created_at",)
    list_per_page = 20
    readonly_fields = ("ip_address", "user_agent", "created_at", "updated_at")

    fieldsets = (
        ("Thông tin liên hệ", {
            "fields": ("full_name", "email", "subject", "message")
        }),
        ("Trạng thái", {
            "fields": ("status", "admin_notes", "replied_at")
        }),
        ("Thông tin kỹ thuật", {
            "fields": ("ip_address", "user_agent"),
            "classes": ("collapse",)
        }),
        ("Thời gian", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def has_add_permission(self, request):
        # Không cho phép tạo contact từ admin (chỉ từ API)
        return False

# Register your models here.
admin.site.register(Links, LinksAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Contact, ContactAdmin)