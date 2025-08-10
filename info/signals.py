from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from info.models import Blogs, Projects
from utils.versioned_cache import VersionedCacheManager

@receiver([post_save, post_delete], sender=Blogs)
def invalidate_blogs_cache(sender, instance, created=None, **kwargs):
    """
    Invalidate cache for blogs

    Args:
        sender:
        instance:
        created:
        **kwargs:

    Returns:

    """
    signal_type = "created" if created else "updated" if created is False else "deleted"
    print(f"Signal received: Blog {instance.id} {signal_type}")

    # Increment version for blogs
    VersionedCacheManager.increment_version("blogs")

    # Increment version for related models
    # VersionedCacheManager.increment_version("files")
    VersionedCacheManager.increment_version("skills")

@receiver([post_save, post_delete], sender=Projects)
def invalidate_projects_cache(sender, instance, created=None, **kwargs):
    """
    Invalidate cache for projects

    Args:
        sender:
        instance:
        created:
        **kwargs:

    Returns:

    """
    signal_type = "created" if created else "updated" if created is False else "deleted"
    print(f"Signal received: Project {instance.id} {signal_type}")

    # Increment version for projects
    VersionedCacheManager.increment_version("projects")

    # Increment version for related models
    # VersionedCacheManager.increment_version("files")
    VersionedCacheManager.increment_version("skills")

def invalidate_experiences_cache(sender, instance, created=None, **kwargs):
    """
    Invalidate cache for experiences

    Args:
        sender:
        instance:
        created:
        **kwargs:

    Returns:

    """
    signal_type = "created" if created else "updated" if created is False else "deleted"
    print(f"Signal received: Experience {instance.id} {signal_type}")

    # Increment version for experiences
    VersionedCacheManager.increment_version("experiences")

    # Increment version for related models
    # VersionedCacheManager.increment_version("files")