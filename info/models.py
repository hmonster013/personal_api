from ckeditor.fields import RichTextField
from django.db import models

from common.models import Links, Skills, File

class InfoBaseModel(models.Model):
    class Meta:
        abstract =  True
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Blogs(InfoBaseModel):
    title = models.CharField(max_length=255)
    content = RichTextField()
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    cover_img = models.OneToOneField(File, null=True, on_delete=models.CASCADE, related_name="personal_info_blogs_cover_img")
    
    skills = models.ManyToManyField(Skills, related_name="personal_info_blogs_skills")
    class Meta:
        db_table = "personal_info_blogs"
        verbose_name_plural = "Blogs"
    
    def __str__(self):
        return self.title
        
class Experiences(InfoBaseModel):
    company_img = models.OneToOneField(File, null=True, on_delete=models.CASCADE, related_name="personal_info_experiences_company_img")
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = RichTextField()
    working_period = models.CharField(max_length=255)
    join_date = models.DateField(null=True)
    leave_date = models.DateField(null=True)
    
    class Meta:
        db_table = "personal_info_experiences"
        verbose_name_plural = "Experiences"
    
    def __str__(self):
        return self.company_name + ' - ' + self.job_title
        
class Projects(InfoBaseModel):
    name = models.CharField(max_length=255)
    descriptions = models.CharField(max_length=255)
    link_github = models.OneToOneField(Links, on_delete=models.CASCADE, related_name="personal_info_projects_github")
    link_website = models.OneToOneField(Links, on_delete=models.CASCADE, related_name="personal_info_projects_website")
    skills = models.ManyToManyField(Skills, related_name="personal_info_experiences")
    
    class Meta:
        db_table = "personal_info_projects"
        verbose_name_plural = "Projects"    
    
    def __str__(self):
        return self.name
    
class ProjectImage(models.Model):
    project = models.ForeignKey(
        'Projects',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Image for {self.project.name}"

    class Meta:
        db_table = 'personal_info_project_images'
        verbose_name_plural = 'Project Images'