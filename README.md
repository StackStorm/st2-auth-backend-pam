# PAM authentication plugin for StackStorm Community and Enterprise edition

[![Build Status](https://travis-ci.org/StackStorm/st2-auth-backend-pam.svg?branch=master)](https://travis-ci.org/StackStorm/st2-auth-backend-pam) [![IRC](https://img.shields.io/irc/%23stackstorm.png)](http://webchat.freenode.net/?channels=stackstorm)

### Requirements

Ubuntu:
```
sudo apt-get -y install libpam0g
```

### Configuration Example

Please refer to the authentication section in the StackStorm 
[documentation](http://docs.stackstorm.com) for basic setup concept. The following is an
example of the auth section in the StackStorm configuration file for the PAM backend.

```
[auth]
mode = standalone
backend = pam
enable = True
use_ssl = True
cert = /path/to/ssl/cert/file
key = /path/to/ssl/key/file
logging = /etc/st2/logging.auth.conf
api_url = https://myhost.examples.com:9101
debug = False
```

## Copyright, License, and Contributors Agreement

Copyright 2015 StackStorm, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in
compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file,
or at: [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
