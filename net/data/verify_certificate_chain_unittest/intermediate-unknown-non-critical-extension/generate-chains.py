#!/usr/bin/python3
# Copyright 2015 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Certificate chain where the intermediate contains an unknown non-critical
extension."""

import sys
sys.path += ['../..']

import gencerts

# Self-signed root certificate.
root = gencerts.create_self_signed_root_certificate('Root')
intermediate = gencerts.create_intermediate_certificate('Intermediate', root)

# Intermediate that has an unknown non-critical extension.
intermediate.get_extensions().add_property('1.2.3.4', 'DER:01:02:03:04')

# Target certificate.
target = gencerts.create_end_entity_certificate('Target', intermediate)

chain = [target, intermediate, root]
gencerts.write_chain(__doc__, chain, 'chain.pem')
