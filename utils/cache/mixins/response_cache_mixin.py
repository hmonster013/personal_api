from rest_framework.response import Response
from utils.cache.managers.response_cache import ResponseCacheManager
from utils.cache.managers.versioned_cache import VersionedCacheManager


class ResponseCacheMixin:
    """
    Mixin for caching API responses with versioning support
    
    This mixin automatically caches successful responses and serves them
    on subsequent requests until the data version changes.
    
    Attributes:
        response_cache_timeout (int): Cache timeout in seconds (default: 300)
    """
    response_cache_timeout = 300

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to handle response caching
        
        Args:
            request: HTTP request object
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Response: Cached or fresh response
        """
        if request.method != 'GET':
            return super().dispatch(request, *args, **kwargs)

        model_name = self.queryset.model.__name__.lower()
        view_name = self.__class__.__name__

        cached_response = ResponseCacheManager.get_versioned_cached_response(
            request=request,
            model_name=model_name,
            view_name=view_name
        )

        if cached_response:
            version = VersionedCacheManager.get_current_version(model_name)
            print(f"Using versioned response cache for {view_name} v{version} ")
            
            # Create proper Response object with renderer context
            response = Response(
                data=cached_response["data"],
                status=cached_response["status_code"]
            )
            # Set renderer context from the view
            response.accepted_renderer = self.get_renderers()[0]
            response.accepted_media_type = response.accepted_renderer.media_type
            response.renderer_context = self.get_renderer_context()
            return response

        print(f"Computing fresh response for {view_name}")
        response = super().dispatch(request, *args, **kwargs)

        if response.status_code == 200:
            ResponseCacheManager.cache_versioned_response(
                request=request,
                model_name=model_name,
                response_data=response.data,
                status_code=response.status_code,
                timeout=self.response_cache_timeout,
                view_name=view_name
            )
            version = VersionedCacheManager.get_current_version(model_name)
            print(f"Stored versioned response cache for {view_name} v{version}")

        return response

