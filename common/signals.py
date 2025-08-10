from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from common.models import File
from utils.cache.managers.versioned_cache import VersionedCacheManager


@receiver([post_save, post_delete], sender=File)
def invalidate_files_cache(sender, instance, created=None, **kwargs):
    """
    Invalidate cache for files when File model changes
    """
    signal_type = "created" if created else "updated" if created is False else "deleted"
    print(f"Signal received: File {instance.id} {signal_type}")

    # Increment version for files
    VersionedCacheManager.increment_version("files")