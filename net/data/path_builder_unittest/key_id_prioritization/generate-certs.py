#!/usr/bin/python3
# Copyright 2019 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A chain with multiple intermediates with different subjectKeyIdentifiers and
notBefore dates, for testing path bulding prioritization.
"""

import sys
sys.path += ['../..']

import gencerts

DATE_A = '150101120000Z'
DATE_B = '150102120000Z'
DATE_C = '150103120000Z'
DATE_Z = '180101120000Z'


root = gencerts.create_self_signed_root_certificate('Root')
root.set_validity_range(DATE_A, DATE_Z)

int_matching_ski_a = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_matching_ski_a.set_validity_range(DATE_A, DATE_Z)

int_matching_ski_b = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_matching_ski_b.set_validity_range(DATE_B, DATE_Z)
int_matching_ski_b.set_key(int_matching_ski_a.get_key())

int_matching_ski_c = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_matching_ski_c.set_validity_range(DATE_C, DATE_Z)
int_matching_ski_c.set_key(int_matching_ski_a.get_key())

# For some reason, OpenSSL seems to require disabling SKID and AKID on the
# parent cert in order to generate an intermediate cert without a SKID.
root2 = gencerts.create_self_signed_root_certificate('Root')
root2.set_key(root.get_key())
section = root2.config.get_section('signing_ca_ext')
section.remove_property('subjectKeyIdentifier')
section.remove_property('authorityKeyIdentifier')

int_no_ski_a = gencerts.create_intermediate_certificate('Intermediate', root2)
int_no_ski_a.set_validity_range(DATE_A, DATE_Z)
int_no_ski_a.set_key(int_matching_ski_a.get_key())
section = int_no_ski_a.config.get_section('req_ext')
section.remove_property('subjectKeyIdentifier')

int_no_ski_b = gencerts.create_intermediate_certificate('Intermediate', root2)
int_no_ski_b.set_validity_range(DATE_B, DATE_Z)
int_no_ski_b.set_key(int_matching_ski_a.get_key())
section = int_no_ski_b.config.get_section('req_ext')
section.remove_property('subjectKeyIdentifier')

int_no_ski_c = gencerts.create_intermediate_certificate('Intermediate', root2)
int_no_ski_c.set_validity_range(DATE_C, DATE_Z)
int_no_ski_c.set_key(int_matching_ski_a.get_key())
section = int_no_ski_c.config.get_section('req_ext')
section.remove_property('subjectKeyIdentifier')

int_different_ski_a = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_different_ski_a.set_validity_range(DATE_A, DATE_Z)

int_different_ski_b = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_different_ski_b.set_validity_range(DATE_B, DATE_Z)
int_different_ski_b.set_key(int_different_ski_a.get_key())

int_different_ski_c = gencerts.create_intermediate_certificate('Intermediate',
                                                              root)
int_different_ski_c.set_validity_range(DATE_C, DATE_Z)
int_different_ski_c.set_key(int_different_ski_a.get_key())

target = gencerts.create_end_entity_certificate('Target', int_matching_ski_a)
target.set_validity_range(DATE_A, DATE_Z)


gencerts.write_chain('The root', [root], out_pem='root.pem')

gencerts.write_chain(
    'Intermediate with matching subjectKeyIdentifier and notBefore A',
    [int_matching_ski_a], out_pem='int_matching_ski_a.pem')

gencerts.write_chain(
    'Intermediate with matching subjectKeyIdentifier and notBefore B',
    [int_matching_ski_b], out_pem='int_matching_ski_b.pem')

gencerts.write_chain(
    'Intermediate with matching subjectKeyIdentifier and notBefore C',
    [int_matching_ski_c], out_pem='int_matching_ski_c.pem')

gencerts.write_chain(
    'Intermediate with no subjectKeyIdentifier and notBefore A',
    [int_no_ski_a], out_pem='int_no_ski_a.pem')

gencerts.write_chain(
    'Intermediate with no subjectKeyIdentifier and notBefore B',
    [int_no_ski_b], out_pem='int_no_ski_b.pem')

gencerts.write_chain(
    'Intermediate with no subjectKeyIdentifier and notBefore C',
    [int_no_ski_c], out_pem='int_no_ski_c.pem')

gencerts.write_chain(
    'Intermediate with different subjectKeyIdentifier and notBefore A',
    [int_different_ski_a], out_pem='int_different_ski_a.pem')

gencerts.write_chain(
    'Intermediate with different subjectKeyIdentifier and notBefore B',
    [int_different_ski_b], out_pem='int_different_ski_b.pem')

gencerts.write_chain(
    'Intermediate with different subjectKeyIdentifier and notBefore C',
    [int_different_ski_c], out_pem='int_different_ski_c.pem')

gencerts.write_chain('The target', [target], out_pem='target.pem')

