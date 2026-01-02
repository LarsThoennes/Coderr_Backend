from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for API endpoints that return large result sets.
    
    Attributes:
    - page_size: Default number of items per page (1)
    - page_size_query_param: Allows clients to set custom page size via query parameter 'page_size'
    - max_page_size: Maximum allowed page size is 10
    """
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10