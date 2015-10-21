# PAM authentication plugin for StackStorm Community and Enterprise edition

[![Build Status](https://travis-ci.org/StackStorm/st2-auth-backend-pam.svg?branch=master)](https://travis-ci.org/StackStorm/st2-auth-backend-pam) [![IRC](https://img.shields.io/irc/%23stackstorm.png)](http://webchat.freenode.net/?channels=stackstorm)

### Requirements

Ubuntu:
```
sudo apt-get -y install libpam0g
```

### Configuration Example

Please refer to the [standalone mode](http://docs.stackstorm.com/config/authentication.html#setup-
standalone-mode) in the configuration section for authentication for basic setup concept. The
following is an example of the auth section in the StackStorm configuration file for the PAM
backend.

```
[auth]
mode = standalone
backend = pam
enable = True
use_ssl = True
cert = /path/to/ssl/cert/file
key = /path/to/ssl/key/file
logging = /path/to/st2auth.logging.conf
api_url = https://myhost.examples.com:9101
debug = False
```
