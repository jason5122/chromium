#!/usr/bin/python3
# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Certificate chain with inhibitAnyPolicy on the root, and an intermediate
that uses anyPolicy. Should fail if the policyConstraints on the root are
enforced."""

import sys
sys.path += ['../..']

import gencerts

# Self-signed root certificate.
root = gencerts.create_self_signed_root_certificate('Root')
root.get_extensions().set_property('inhibitAnyPolicy', 'critical,0')

# Intermediate certificate.
intermediate = gencerts.create_intermediate_certificate('Intermediate', root)
intermediate.get_extensions().set_property('policyConstraints',
                                           'critical,requireExplicitPolicy:0')

intermediate.get_extensions().set_property('certificatePolicies',
                                           'critical,anyPolicy')

# Target certificate.
target = gencerts.create_end_entity_certificate('Target', intermediate)
target.get_extensions().set_property('certificatePolicies', 'critical,1.2.3.5')

chain = [target, intermediate, root]
gencerts.write_chain(__doc__, chain, 'chain.pem')
