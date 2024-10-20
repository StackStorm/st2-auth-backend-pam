# -*- coding: utf-8 -*-
# The pam components have been modified to be salty and have been taken from
# the pam module under this licence:
# (c) 2007 Chris AtLee <chris@atlee.ca>
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php
'''
Authenticate against PAM

Provides an authenticate function that will allow the caller to authenticate
a user against the Pluggable Authentication Modules (PAM) on the system.

Implemented using ctypes, so no compilation is necessary.

.. note:: PAM authentication will not work for the ``root`` user.

    The Python interface to PAM does not support authenticating as ``root``.

'''

# Import Python Libs
from __future__ import absolute_import
from ctypes import CDLL, POINTER, Structure, CFUNCTYPE, cast, sizeof, byref
from ctypes import c_void_p, c_uint, c_char_p, c_char, c_int
from ctypes import memmove
from ctypes.util import find_library

LIBPAM = CDLL(find_library('pam'))
LIBC = CDLL(find_library('c'))

CALLOC = LIBC.calloc
CALLOC.restype = c_void_p
CALLOC.argtypes = [c_uint, c_uint]

STRDUP = LIBC.strdup
STRDUP.argstypes = [c_char_p]
STRDUP.restype = POINTER(c_char)  # NOT c_char_p !!!!

# Various constants
PAM_PROMPT_ECHO_OFF = 1
PAM_PROMPT_ECHO_ON = 2
PAM_ERROR_MSG = 3
PAM_TEXT_INFO = 4


class PamHandle(Structure):
    '''
    Wrapper class for pam_handle_t
    '''
    _fields_ = [
        ('handle', c_void_p)
    ]

    def __init__(self):
        Structure.__init__(self)
        self.handle = 0


class PamMessage(Structure):
    '''
    Wrapper class for pam_message structure
    '''
    _fields_ = [
        ("msg_style", c_int),
        ("msg", c_char_p),
    ]

    def __repr__(self):
        return '<PamMessage {0} \'{1}\'>'.format(self.msg_style, self.msg)


class PamResponse(Structure):
    '''
    Wrapper class for pam_response structure
    '''
    _fields_ = [
        ('resp', c_char_p),
        ('resp_retcode', c_int),
    ]

    def __repr__(self):
        return '<PamResponse {0} \'{1}\'>'.format(self.resp_retcode, self.resp)


CONV_FUNC = CFUNCTYPE(
    c_int,
    c_int, POINTER(POINTER(PamMessage)),
    POINTER(POINTER(PamResponse)), c_void_p
)


class PamConv(Structure):
    '''
    Wrapper class for pam_conv structure
    '''
    _fields_ = [
        ('conv', CONV_FUNC),
        ('appdata_ptr', c_void_p)
    ]


try:
    PAM_START = LIBPAM.pam_start
    PAM_START.restype = c_int
    PAM_START.argtypes = [
        c_char_p, c_char_p, POINTER(PamConv),
        POINTER(PamHandle)
    ]

    PAM_AUTHENTICATE = LIBPAM.pam_authenticate
    PAM_AUTHENTICATE.restype = c_int
    PAM_AUTHENTICATE.argtypes = [PamHandle, c_int]

    PAM_END = LIBPAM.pam_end
    PAM_END.restype = c_int
    PAM_END.argtypes = [PamHandle, c_int]
except Exception:
    HAS_PAM = False
else:
    HAS_PAM = True


def __virtual__():
    '''
    Only load on Linux systems
    '''
    return HAS_PAM


def authenticate(username, password, service='login'):
    '''
    Returns True if the given username and password authenticate for the
    given service.  Returns False otherwise

    ``username``: the username to authenticate

    ``password``: the password in plain text

    ``service``: the PAM service to authenticate against.
                 Defaults to 'login'
    '''
    @CONV_FUNC
    def my_conv(n_messages, messages, p_response, app_data):
        '''
        Simple conversation function that responds to any
        prompt where the echo is off with the supplied password
        '''
        # Create an array of n_messages response objects
        addr = CALLOC(n_messages, sizeof(PamResponse))
        response = cast(addr, POINTER(PamResponse))
        p_response[0] = response
        for i in range(n_messages):
            if messages[i].contents.msg_style == PAM_PROMPT_ECHO_OFF:
                dst = CALLOC(len(password) + 1, sizeof(c_char))
                memmove(dst, cpassword, len(password))
                response[i].resp = dst
                response[i].resp_retcode = 0
        return 0

    username = username.encode('UTF-8')
    password = password.encode('UTF-8')
    service = service.encode('UTF-8')
    cpassword = c_char_p(password)
    handle = PamHandle()
    conv = PamConv(my_conv, 0)
    retval = PAM_START(service, username, byref(conv), byref(handle))

    if retval != 0:
        # TODO: This is not an authentication error, something
        # has gone wrong starting up PAM
        PAM_END(handle, retval)
        return False

    retval = PAM_AUTHENTICATE(handle, 0)
    PAM_END(handle, 0)
    return retval == 0


def auth(username, password, service='login'):
    '''
    Authenticate via pam
    '''
    return authenticate(username=username, password=password, service=service)
