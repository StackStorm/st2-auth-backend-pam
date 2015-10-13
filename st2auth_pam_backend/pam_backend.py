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

import logging

__all__ = [
    'PAMAuthenticationBackend'
]

from st2auth_pam_backend.pam_ffi import auth as pam_auth

LOG = logging.getLogger(__name__)


class PAMAuthenticationBackend(object):
    """
    PAM module for python

    Provides an authenticate function that will allow the caller to
    authenticate a user against the Pluggable Authentication Modules
    (PAM) on the system.

    pam_ffi is implemented using ctypes, so no compilation is necessary.
    """

    def __init__(self):
        pass

    def authenticate(self, username, password):
        try:
            return pam_auth(username, password)
            LOG.info('Successfully authenticated user "%s".', username)
        except:
            LOG.exception('Failed authenticating user "%s".', username)


if __name__ == "__main__":
    import getpass
    pam = PAMAuthenticationBackend()
    user = raw_input('Username: ')
    print(pam.authenticate(user, getpass.getpass()))
