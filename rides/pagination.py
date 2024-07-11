from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100  # Adjust the max page size as needed