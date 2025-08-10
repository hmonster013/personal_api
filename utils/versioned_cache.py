from django.core.cache import cache


class VersionedCacheManager:
    @staticmethod
    def get_version_key(model_name):
        """Generate cache key for model version

        Args:
            model_name (str): Name of the model

        Returns:
            str: Cache key
        """
        return f"version_{model_name}"

    @staticmethod
    def get_current_version(model_name):
        """Get current version of a model

        Args:
            model_name (str): Name of the model

        Returns:
            int: Current version
        """
        return cache.get(VersionedCacheManager.get_version_key(model_name)) or 1

    @staticmethod
    def increment_version(model_name):
        """
        Increment version of a model

        Args:
            model_name:

        Returns:

        """
        version_key = VersionedCacheManager.get_version_key(model_name)
        current_version = cache.get(version_key) or 1
        new_version = current_version + 1
        cache.set(version_key, new_version)
        print(f"Version incremented: {model_name} v{current_version} -> v{new_version}")
        return new_version

    @staticmethod
    def get_versioned_key(base_key, model_name):
        """Generate versioned cache key

        Args:
            base_key (str): Base cache key
            model_name (str): Name of the model

        Returns:
            str: Versioned cache key
        """
        version = VersionedCacheManager.get_current_version(model_name)
        return f"{base_key}_v{version}"

    @staticmethod
    def get_versioned_data(base_key, model_name):
        """Get versioned data

        Args:
            base_key (str): Base cache key
            model_name (str): Name of the model

        Returns:
            any: Cached data
        """
        versioned_key = VersionedCacheManager.get_versioned_key(base_key, model_name)
        return cache.get(versioned_key)

    @staticmethod
    def set_versioned_data(base_key, model_name, data, timeout=None):
        """Set versioned data

        Args:
            base_key (str): Base cache key
            model_name (str): Name of the model
            data (any): Data to cache
            timeout (int, optional): Timeout in seconds. Defaults to None.

        Returns:
            any: Cached data
        """
        versioned_key = VersionedCacheManager.get_versioned_key(base_key, model_name)
        cache.set(versioned_key, data, timeout=timeout)
        print(f"Versioned cache stored: {versioned_key[:50]}...")
        return versioned_key