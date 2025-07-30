from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from ckeditor.widgets import CKEditorWidget

from common.models import File
from helpers.cloudinary_service import CloudinaryService
from .models import Blogs, Experiences, ProjectImage, Projects
from django.db import models

class BlogAdminForm(forms.ModelForm):
    cover_image = forms.ImageField(label="Cover Image", required=False)

    class Meta:
        model = Blogs
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        cover_image = self.cleaned_data.get('cover_image')

        if cover_image:
            upload_result = CloudinaryService.upload_image(
                file=cover_image,
                folder=settings.CLOUDINARY_DIRECTORY["blog_cover_image"],
                options={'resource_type': "image"}
            )
            if upload_result:
                if instance.cover_img:
                    CloudinaryService.delete_image(instance.cover_img.public_id)
                    instance.cover_img.delete()

                file_instance = File.update_or_create_file_with_cloudinary(
                    file=None,
                    cloudinary_upload_result=upload_result,
                    file_type=File.BLOG_TYPE
                )
                instance.cover_img = file_instance

        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class BlogsAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    
    list_display = ("id", "title", "display_cover_img", "description", "status", "display_skills")
    list_display_links = ("id", "title")
    search_fields = ("title", "description")
    ordering = ("id",)
    list_per_page = 5
    
    fields = (
        "title", 
        "content", 
        "description", 
        "status", 
        "display_cover_img",
        "cover_image", 
        "skills"
    )
    
    readonly_fields = ("display_cover_img",)
    
    def display_skills(self, obj):
        if obj and obj.skills.exists():
            skills_html = [
                f'<span style="display: inline-flex; align-items: center; gap: 5px;">'
                f'<span style="width: 24px; height: 24px; display: inline-block;">{skill.icon}</span>'
                f'<span>{skill.name}</span>'
                f'</span>'
                for skill in obj.skills.all()
            ]
            return mark_safe(", ".join(skills_html))
        return "No skills"

    display_skills.short_description = "Selected Skills"
    
    def display_cover_img(self, obj):
        if obj.cover_img:
            return mark_safe(f'<img src="{obj.cover_img.get_full_url()}" style="max-width: 250px; max-height: 250px;">')
        return "No image"
    
    display_cover_img.short_description = "Current Cover Image"
          
class ExperiencesAdminForm(forms.ModelForm):
    company_image = forms.ImageField(label="Company Image", required=False)

    class Meta:
        model = Experiences
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        company_image = self.cleaned_data.get('company_image')

        if company_image:
            upload_result = CloudinaryService.upload_image(
                file=company_image,
                folder=settings.CLOUDINARY_DIRECTORY["company_image"],
                options={'resource_type': "image"}
            )
            if upload_result:
                if instance.company_img:
                    CloudinaryService.delete_image(instance.company_img.public_id)
                    instance.company_img.delete()

                file_instance = File.update_or_create_file_with_cloudinary(
                    file=None,
                    cloudinary_upload_result=upload_result,
                    file_type=File.EXPERIENCE_TYPE
                )
                instance.company_img = file_instance

        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class ExperiencesAdmin(admin.ModelAdmin):
    form = ExperiencesAdminForm
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    
    list_display = (
        "id", "company_name", "display_company_img", 
        "job_title", "display_description", "working_period", 
        "join_date", "leave_date")
    list_display_links = ("id", "company_name")
    search_fields = ("company_name", "job_title", "description")
    ordering = ("created_at",)
    list_per_page = 5
    
    fields = (
        "company_name",
        "display_company_img",
        "company_image", 
        "job_title", 
        "description", 
        "working_period",
        "join_date",
        "leave_date",
        "created_at",
        "updated_at"
    )
    
    readonly_fields = ("display_company_img", "created_at", "updated_at")
    
    def display_description(self, obj):
        if obj.description:
            return mark_safe(obj.description)
        return "No description"
    
    display_description.short_description = "Current Description"
    
    def display_company_img(self, obj):
        if obj.company_img:
            return mark_safe(f'<img src="{obj.company_img.get_full_url()}" style="max-width: 100px; max-height: 100px;">')
        return "No image"
    
    display_company_img.short_description = "Current Company Image"
    
class ProjectImageInlineForm(forms.ModelForm):
    image_file = forms.ImageField(label="Upload Image", required=False)

    class Meta:
        model = ProjectImage
        fields = ['image_file']

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_file')

        if image_file:
            project_id = instance.project.id if instance.project else "unknown"
            folder = (
                f"{settings.CLOUDINARY_DIRECTORY['project_image']}"
                f"/{project_id}/"
            )

            # Tải ảnh lên Cloudinary
            upload_result = CloudinaryService.upload_image(
                file=image_file,
                folder=folder,
                options={'resource_type': "image"}
            )
            if upload_result:
                # Xóa ảnh cũ nếu có
                if instance.image:
                    CloudinaryService.delete_image(instance.image.public_id)
                    instance.image.delete()

                # Tạo bản ghi File mới
                file_instance = File.update_or_create_file_with_cloudinary(
                    file=None,
                    cloudinary_upload_result=upload_result,
                    file_type=File.PROJECT_TYPE
                )
                instance.image = file_instance

        if commit:
            instance.save()
        return instance


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    form = ProjectImageInlineForm
    extra = 1
    max_num = 5
    fields = ('image_file', 'display_image')
    readonly_fields = ('display_image',)

    def display_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.get_full_url()}" style="max-width: 150px; max-height: 150px;">'
            )
        return "No image"

    display_image.short_description = "Image Preview"


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_images", "descriptions")
    list_display_links = ("id", "name")
    search_fields = ("name", "descriptions")
    ordering = ("id",)
    list_per_page = 5
    inlines = [ProjectImageInline]

    fields = (
        "name",
        "descriptions",
        "link_github",
        "link_website",
        "skills",
    )

    def display_images(self, obj):
        if obj and obj.images.exists():
            images_html = [
                f'<img src="{image.image.get_full_url()}" style="max-width: 100px; max-height: 100px; margin-right: 5px;">'
                for image in obj.images.all()
            ]
            return mark_safe("".join(images_html))
        return "No images"

    display_images.short_description = "Project Images"
    
# Register your models here.
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Experiences, ExperiencesAdmin)
admin.site.register(Projects, ProjectsAdmin)