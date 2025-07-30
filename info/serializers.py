from rest_framework import serializers

from common.serializers import FileSerializer, LinksSerializer, SkillsSerializer
from info.models import Blogs, Experiences, ProjectImage, Projects

class BlogsSerializer(serializers.ModelSerializer):
    cover_img = FileSerializer(read_only=True)
    skills = SkillsSerializer(many=True, read_only=True)

    class Meta:
        model = Blogs
        fields = ['id', 'title', 'content', 
                  'description', 'status', 'cover_img', 
                  'skills']

class ExperiencesSerializer(serializers.ModelSerializer):
    company_img = FileSerializer(read_only=True)
    
    class Meta:
        model = Experiences
        fields = ['id', 'company_img', 'company_name',
                  'job_title', 'description', 'working_period',
                  'join_date', 'leave_date']

class ProjectImageSerializer(serializers.ModelSerializer):
    image = FileSerializer(read_only=True)
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectsSerializer(serializers.ModelSerializer):
    link_github = LinksSerializer(read_only=True)
    link_website = LinksSerializer(read_only=True)
    skills = SkillsSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projects
        fields = ['id', 'name', 'descriptions',
                  'link_github', 'link_website', 'skills',
                  'images']
