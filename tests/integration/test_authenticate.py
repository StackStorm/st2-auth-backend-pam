# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import unittest2

from st2auth_pam_backend import pam_backend


class PAMBackendAuthenticationTest(unittest2.TestCase):
    @mock.patch('os.geteuid')
    def test_non_root_user(self, mock_get_euid):
        # non root
        mock_get_euid.return_value = 100

        expected_msg = 'st2auth process needs to run as "root"'
        self.assertRaisesRegexp(ValueError, expected_msg,
                                pam_backend.PAMAuthenticationBackend)

        # non root, but check for root is disabled
        mock_get_euid.return_value = 100
        pam_backend.PAMAuthenticationBackend(check_for_root=False)

        # root
        mock_get_euid.return_value = 0
        pam_backend.PAMAuthenticationBackend()

    # See scrips/travis/prepare-integration.sh for right username + password.
    @mock.patch('os.geteuid', mock.Mock(return_value=0))
    def test_good_password(self):
        pam = pam_backend.PAMAuthenticationBackend()
        self.assertEqual(pam.authenticate('pammer', 'spammer'), True,
                         'Valid credentials should return True.')

    # See scrips/travis/prepare-integration.sh for right username + password.
    @mock.patch('os.geteuid', mock.Mock(return_value=0))
    def test_bad_password(self):
        pam = pam_backend.PAMAuthenticationBackend()
        self.assertEqual(pam.authenticate('pammer', 'oumpalumpa'), False,
                         'Invalid credentials should return False.')
