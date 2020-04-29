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

from __future__ import absolute_import

import os
import logging

__all__ = [
    'PAMAuthenticationBackend'
]

from st2auth_pam_backend.pam_ffi import auth as pam_auth

LOG = logging.getLogger(__name__)

PAM_DOCS_LINK = 'https://docs.stackstorm.com/install/deb.html#configure-authentication'
NON_ROOT_ERROR_MSG = ('When using pam backend, st2auth process needs to run as "root" so it can '
                      'read /etc/shadow file. For more details, please see %s' %
                      (PAM_DOCS_LINK))


class PAMAuthenticationBackend(object):
    """
    PAM module for python

    Provides an authenticate function that will allow the caller to
    authenticate a user against the Pluggable Authentication Modules
    (PAM) on the system.

    pam_ffi is implemented using ctypes, so no compilation is necessary.
    """

    def __init__(self, service='login', check_for_root=True):
        """
        :param service: PAM service to authenticate against.
        :type service: ``str``

        :param check_for_root: True to check that the current process is running as root (uid 0).
        :type check_for_root: ``bool``
        """
        self._service = service

        if check_for_root:
            self._verify_running_as_root()

    def authenticate(self, username, password):
        try:
            ret = pam_auth(username=username, password=password, service=self._service)

            if ret:
                LOG.info('Successfully authenticated user "%s".', username)
            else:
                LOG.info('Invalid username/password for user "%s".', username)

            return ret
        except Exception:
            LOG.exception('Unable to PAM authenticate user "%s".', username)
            raise

        return False

    def _verify_running_as_root(self):
        uid = os.geteuid()

        if uid != 0:
            raise ValueError(NON_ROOT_ERROR_MSG)
