import pickle
from unittest import TestCase
from unittest.mock import patch

from django.conf import settings
from django.core.cache import cache
from places.wrappers import CacheableWrapper


class GoogleMapClientMock:
    class_attr = 1

    def __init__(self):
        self.inst_attr = '2'

    def inst_method_without_args(self):
        return 13

    def inst_method_with_args(self, a1, a2):
        return 'result'


class CacheableWrapperTests(TestCase):
    def setUp(self):
        self.inner_client = GoogleMapClientMock()
        self.client = CacheableWrapper(self.inner_client)

    def test_call_inner_client_existing_method_with_args(self):
        expected_result = self.inner_client.inst_method_with_args('text',
                                                                  a2='142')

        self.assertEqual(
            self.client.inst_method_with_args('text', a2='142'),
            expected_result
        )

    def test_call_inner_client_existing_method_without_args(self):
        expected_result = self.inner_client.inst_method_without_args()

        self.assertEqual(
            self.client.inst_method_without_args(),
            expected_result
        )

    def test_get_inner_client_instance_existing_attr(self):
        expected_result = self.inner_client.inst_attr

        self.assertEqual(self.client.inst_attr, expected_result)

    def test_get_inner_client_class_existing_attr(self):
        expected_result = self.inner_client.class_attr

        self.assertEqual(self.client.class_attr, expected_result)

    def test_call_inner_client_non_existent_method(self):
        with self.assertRaises(AttributeError):
            self.client.non_existent_method('text', a2='142')

    def test_call_inner_client_non_existent_attr(self):
        with self.assertRaises(AttributeError):
            self.client.non_existent_attr

    def test_cache_set__method_call(self):
        key = "inst_method_with_args::('text',)::{'a2': '142'}"
        data = pickle.dumps('result')


        with patch.object(cache, 'set') as cache_mock:
            self.client.inst_method_with_args('text', a2='142')

        cache_mock.assert_called_once_with(key, data, settings.CACHING_TIME)

    def test_cache_set__attr_get(self):
        with patch.object(cache, 'set') as cache_mock:
            self.client.inst_attr

        cache_mock.assert_not_called()

    def test_cache_get__before_data_were_cached__method_call(self):
        key = "inst_method_with_args::('text',)::{'a2': '142'}"

        with patch.object(cache, 'get', return_value=None) as cache_mock:
            self.client.inst_method_with_args('text', a2='142')

        cache_mock.assert_called_once_with(key)

    def test_cache_get__after_data_were_cached__method_call(self):
        key = "inst_method_with_args::('text',)::{'a2': '142'}"
        data = pickle.dumps('result')

        with patch.object(cache, 'get', return_value=data) as cache_mock:
            self.client.inst_method_with_args('text', a2='142')

        cache_mock.assert_called_once_with(key)
