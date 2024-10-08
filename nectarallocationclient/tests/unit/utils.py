#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
from unittest import mock

import fixtures
import requests
from requests_mock.contrib import fixture as requests_mock_fixture
import testtools


def _patch_mock_to_raise_for_invalid_assert_calls():
    def raise_for_invalid_assert_calls(wrapped):
        def wrapper(_self, name):
            valid_asserts = [
                'assert_called_with',
                'assert_called_once_with',
                'assert_has_calls',
                'assert_any_calls',
            ]

            if name.startswith('assert') and name not in valid_asserts:
                raise AttributeError(
                    f'{name} is not a valid mock assert method'
                )

            return wrapped(_self, name)

        return wrapper

    mock.Mock.__getattr__ = raise_for_invalid_assert_calls(
        mock.Mock.__getattr__
    )


# NOTE(gibi): needs to be called only once at import time
# to patch the mock lib
_patch_mock_to_raise_for_invalid_assert_calls()


class TestCase(testtools.TestCase):
    TEST_REQUEST_BASE = {
        'verify': True,
    }

    def setUp(self):
        super().setUp()
        if (
            os.environ.get('OS_STDOUT_CAPTURE') == 'True'
            or os.environ.get('OS_STDOUT_CAPTURE') == '1'
        ):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if (
            os.environ.get('OS_STDERR_CAPTURE') == 'True'
            or os.environ.get('OS_STDERR_CAPTURE') == '1'
        ):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        self.requests_mock = self.useFixture(requests_mock_fixture.Fixture())

    def assert_request_id(self, request_id_mixin, request_id_list):
        self.assertEqual(request_id_list, request_id_mixin.request_ids)


class TestResponse(requests.Response):
    """Class used to wrap requests.Response.
    Provide some convenience to initialize with a dict.
    """

    def __init__(self, data):
        super().__init__()
        self._text = None
        if isinstance(data, dict):
            self.status_code = data.get('status_code')
            self.headers = data.get('headers')
            # Fake the text attribute to streamline Response creation
            self._text = data.get('text')
        else:
            self.status_code = data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def text(self):
        return self._text
