#!/usr/bin/python3
# Copyright 2022 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Certificate chain where the target certificate sets the extended key usage
to clientAuth. Neither the root nor the intermediate have an EKU."""

import sys
sys.path += ['../..']

import gencerts

# Self-signed root certificate.
root = gencerts.create_self_signed_root_certificate('Root')

# Intermediate certificate.
intermediate = gencerts.create_intermediate_certificate('Intermediate', root)

# Target certificate.
target = gencerts.create_end_entity_certificate('Target', intermediate)
target.get_extensions().set_property('extendedKeyUsage', 'anyExtendedKeyUsage')

chain = [target, intermediate, root]
gencerts.write_chain(__doc__, chain, 'chain.pem')
