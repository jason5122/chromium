#!/usr/bin/python3
# Copyright 2021 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
A chain with a self-signed Root1 and a Root1 cross signed by Root2. The
cross-signed root has a newer notBefore date than the self-signed one.
"""

import sys
sys.path += ['../..']

import gencerts

DATE_A = '150101120000Z'
DATE_B = '150102120000Z'
DATE_Z = '180101120000Z'

root1 = gencerts.create_self_signed_root_certificate('Root1')
root1.set_validity_range(DATE_A, DATE_Z)

root2 = gencerts.create_self_signed_root_certificate('Root2')
root2.set_validity_range(DATE_A, DATE_Z)

root1_cross = gencerts.create_intermediate_certificate('Root1', root2)
root1_cross.set_key(root1.get_key())
root1_cross.set_validity_range(DATE_B, DATE_Z)

target = gencerts.create_end_entity_certificate('Target', root1)
target.set_validity_range(DATE_A, DATE_Z)

gencerts.write_chain('Root1', [root1], out_pem='root1.pem')
gencerts.write_chain('Root2', [root2], out_pem='root2.pem')
gencerts.write_chain(
    'Root1 cross-signed by Root2, with a newer notBefore date'
    ' than Root1', [root1_cross],
    out_pem='root1_cross.pem')
gencerts.write_chain('Target', [target], out_pem='target.pem')
