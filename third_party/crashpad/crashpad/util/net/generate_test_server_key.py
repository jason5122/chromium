#!/usr/bin/python3

# Copyright 2018 The Crashpad Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import sys

testdata = os.path.join(os.path.dirname(__file__), 'testdata')
key = os.path.join(testdata, 'crashpad_util_test_key.pem')
cert = os.path.join(testdata, 'crashpad_util_test_cert.pem')

with open(cert, 'w') as cert_file, open(key, 'w') as key_file:
    MESSAGE = ('DO NOT EDIT: This file was auto-generated by ' + __file__ +
               '\n\n')
    cert_file.write(MESSAGE)
    key_file.write(MESSAGE)

    proc = subprocess.Popen([
        'openssl', 'req', '-x509', '-nodes', '-subj', '/CN=localhost', '-days',
        '3650', '-newkey', 'rsa:2048', '-keyout', '-'
    ],
                            stderr=open(os.devnull, 'w'),
                            stdout=subprocess.PIPE)

    contents = proc.communicate()[0]
    dest = sys.stderr
    for line in contents.splitlines(True):
        if line.startswith("-----BEGIN PRIVATE KEY-----"):
            dest = key_file
        elif line.startswith("-----BEGIN CERTIFICATE-----"):
            dest = cert_file
        elif line.startswith("-----END"):
            dest.write(line)
            dest = sys.stderr
            continue

        dest.write(line)
