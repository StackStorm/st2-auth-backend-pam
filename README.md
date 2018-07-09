# PAM authentication plugin for StackStorm Community and Enterprise edition

[![Build Status](https://travis-ci.org/StackStorm/st2-auth-backend-pam.svg?branch=master)](https://travis-ci.org/StackStorm/st2-auth-backend-pam) [![IRC](https://img.shields.io/irc/%23stackstorm.png)](http://webchat.freenode.net/?channels=stackstorm)

PAM authentication backend allows users to authenticate against the PAM (Pluggable Authentication
Modules) on the system where ``st2auth`` service is running.

### Requirements

Ubuntu:

```bash
sudo apt-get -y install libpam0g
```

RHEL/CentOS:

```
sudo yum -y install pam-devel
```

### Installation

Install this into the ST2 virtualenv with:

```bash
sudo /opt/stackstorm/st2/bin/pip install git+https://github.com/StackStorm/st2-auth-backend-pam.git@master#egg=st2_auth_backend_pam
```

Edit the file: `/lib/systemd/system/st2auth.service`. Modify it so that the `stauth` service runs as root.

### Configuration Options

| option    | required | default | description                                                |
|-----------|----------|---------|------------------------------------------------------------|
| service   | no       | login   | PAM service to authenticate against                        |

### Configuration Example

Please refer to the authentication section in the StackStorm 
[documentation](http://docs.stackstorm.com) for basic setup concept. The following is an
example of the auth section in the StackStorm configuration file for the PAM backend.

```
[auth]
mode = standalone
backend = pam
backend_kwargs = {"service": "login"}
...
```

### Limitations

The python implementation of PAM does not allow authentication as the `root` user.
When utilizing this backend, you will need to authenticate as a non-`root` user.


## Copyright, License, and Contributors Agreement

Copyright 2015 StackStorm, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in
compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file,
or at: [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
