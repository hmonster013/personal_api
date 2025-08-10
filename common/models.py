from django.db import models
from ckeditor.fields import RichTextField

from utils.services.cloudinary_service import CloudinaryService

class CommonBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class File(CommonBaseModel):
    BLOG_TYPE = 'BLOG'
    EXPERIENCE_TYPE = 'EXPERIENCE'
    PROJECT_TYPE = 'PROJECT'
    SYSTEM_TYPE = 'SYSTEM'
    OTHER_TYPE = 'OTHER'
    
    FILE_TYPES = [
        (BLOG_TYPE, 'Blog'),
        (EXPERIENCE_TYPE, 'Experience'),
        (PROJECT_TYPE, 'Project'),
        (SYSTEM_TYPE, 'System'),
        (OTHER_TYPE, 'Other')
    ]
    
    RESOURCE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('raw', 'Raw File'),
    ]
    
    public_id = models.CharField(max_length=255)
    version = models.CharField(max_length=20, null=True, blank=True)
    format = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES, default=OTHER_TYPE)
    uploaded_at = models.DateTimeField(null=False, blank=False)
    metadata = models.JSONField(blank=True, null=True)
    
    def get_full_url(self):
        url, _ = CloudinaryService.get_url_from_public_id(self.public_id, {
            'version': self.version,
            'format': self.format,
            'resource_type': self.resource_type,
        })
        return url
    
    @staticmethod
    def update_or_create_file_with_cloudinary(file, cloudinary_upload_result, file_type: str = OTHER_TYPE):
        file_data = {
            "public_id": cloudinary_upload_result.get("public_id"),
            "version": cloudinary_upload_result.get("version"),
            "format": cloudinary_upload_result.get("format"),
            "resource_type": cloudinary_upload_result.get("resource_type"),
            "uploaded_at": cloudinary_upload_result.get("created_at"),
            "metadata": cloudinary_upload_result,
            "file_type": file_type
        }
        if file:
            # Update file
            for key, value in file_data.items():
                setattr(file, key, value)
            file.save()
        else:
            # Create file
            file = File.objects.create(**file_data)
        return file
    
    class Meta:
        db_table = "personal_common_files"
        verbose_name_plural = "Files"
        ordering = ['-created_at']
        
class Links(CommonBaseModel):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.URLField()
    icon = models.CharField(max_length=255)
    
    class Meta:
        db_table = "personal_common_links"
        verbose_name_plural = "Links"
    
    def __str__(self):
        return self.name
        
class Skills(CommonBaseModel):
    icon = RichTextField()
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'personal_common_skills'
        verbose_name_plural = "Skills"
        
    def __str__(self):
        return self.name

class Contact(CommonBaseModel):
    full_name = models.CharField(max_length=255, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=500, verbose_name="Chủ đề")
    message = models.TextField(verbose_name="Nội dung tin nhắn")
    
    STATUS_CHOICES = [
        ('NEW', 'Mới'),
        ('READ', 'Đã đọc'),
        ('REPLIED', 'Đã phản hồi'),
        ('CLOSED', 'Đã đóng'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Trạng thái")
    
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Địa chỉ IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú admin")
    replied_at = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian phản hồi")
    
    class Meta:
        db_table = "personal_common_contacts"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"