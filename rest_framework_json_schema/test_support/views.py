from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ArtistSerializer, AlbumSerializer, get_artists, get_albums
from rest_framework_json_schema.negotiation import JSONAPIContentNegotiation
from rest_framework_json_schema.pagination import JSONAPILimitOffsetPagination
from rest_framework_json_schema.parsers import JSONAPIParser
from rest_framework_json_schema.renderers import JSONAPIRenderer


class BaseViewSet(viewsets.ModelViewSet):
    parser_classes = (JSONAPIParser,)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONAPIRenderer,)
    content_negotiation_class = JSONAPIContentNegotiation

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try:
            return self.get_queryset()[self.kwargs[lookup_url_kwarg]]
        except IndexError:
            raise Http404('Not found.')


class ArtistViewSet(BaseViewSet):
    """
    A simple ViewSet for listing or retrieving artists.
    """
    serializer_class = ArtistSerializer
    # This is not testing pagination
    pagination_class = None

    parser_classes = (JSONAPIParser,)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONAPIRenderer,)
    content_negotiation_class = JSONAPIContentNegotiation

    def get_queryset(self):
        return get_artists()


class PaginateViewSet(ArtistViewSet):
    pagination_class = JSONAPILimitOffsetPagination


class AlbumViewSet(BaseViewSet):
    """
    A simple ViewSet for listing or retrieving albums.
    """
    serializer_class = AlbumSerializer
    pagination_class = None

    def get_queryset(self):
        return get_albums()

    @detail_route(methods=['get'])
    def relationship_artist(self):
        # Not currently called, just reversed.
        return Response()

    @detail_route(methods=['get'])
    def related_artist(self):
        # Not currently called, just reversed.
        return Response()