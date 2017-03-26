from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APISimpleTestCase, APIRequestFactory

from rest_framework_json_schema.test_support.serializers import reset_data
from rest_framework_json_schema.test_support.views import PaginateViewSet, NonJSONPaginateViewSet


@override_settings(ROOT_URLCONF='rest_framework_json_schema.test_support.urls')
class JSONAPIPaginationTestCase(APISimpleTestCase):
    maxDiff = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view_list = PaginateViewSet.as_view({'get': 'list'})
        self.view_detail = PaginateViewSet.as_view({'get': 'retrieve'})
        reset_data()

    def test_limit_offset(self):
        """
        Pagination works according to spec
        """
        list_url = reverse('page-list')
        request = self.factory.get(list_url, {'offset': 2, 'limit': 2})
        response = self.view_list(request)
        response.render()
        self.assertEqual(response['Content-Type'], 'application/vnd.api+json')

        self.assertJSONEqual(response.content.decode(), {
            'meta': {
                'count': 6
            },
            'links': {
                'page[next]': 'http://testserver%s?limit=2&offset=4' % list_url,
                'page[previous]': 'http://testserver%s?limit=2' % list_url
            },
            'data': [
                {
                    'id': '2',
                    'type': 'artist',
                    'attributes': {'firstName': 'Charles', 'lastName': 'Mingus'}
                },
                {
                    'id': '3',
                    'type': 'artist',
                    'attributes': {'firstName': 'Bill', 'lastName': 'Evans'}
                }
            ]
        })


@override_settings(ROOT_URLCONF='rest_framework_json_schema.test_support.urls')
class JSONAPINonPageTestCase(APISimpleTestCase):
    maxDiff = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view_list = NonJSONPaginateViewSet.as_view({'get': 'list'})
        self.view_detail = NonJSONPaginateViewSet.as_view({'get': 'retrieve'})
        reset_data()

    def test_limit_offset(self):
        list_url = reverse('page-list')
        request = self.factory.get(list_url, {'offset': 2, 'limit': 2})
        response = self.view_list(request)
        with self.assertRaises(ImproperlyConfigured):
            response.render()
