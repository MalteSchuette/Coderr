from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Page-number pagination for the offer list, defaulting to 6 items per page."""

    page_size = 6
    page_size_query_param = 'page_size'