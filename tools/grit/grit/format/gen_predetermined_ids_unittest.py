#!/usr/bin/python3
# Copyright 2017 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

'''Unit tests for the gen_predetermined_ids module.'''

import io
import os
import sys
import unittest

if __name__ == '__main__':
  sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from grit.format import gen_predetermined_ids

class GenPredeterminedIdsUnittest(unittest.TestCase):
  def testGenerateResourceMapping(self):
    original_resources = {200: 'A', 201: 'B', 300: 'C', 350: 'D', 370: 'E'}
    ordered_resource_ids = [300, 201, 370]
    mapping = gen_predetermined_ids.GenerateResourceMapping(
        original_resources, ordered_resource_ids)
    self.assertEqual({101: 'C', 102: 'B', 103: 'E'}, mapping)

  def testReadResourceIdsFromFile(self):
    f = io.StringIO('''
// This file is automatically generated by GRIT. Do not edit.

#pragma once

#define IDS_BOOKMARKS_NO_ITEMS 12500
#define IDS_BOOKMARK_BAR_IMPORT_LINK (::ui::AllowlistedResource<12501>(), 12501)
#define IDS_BOOKMARK_X (::ui::AllowlistedResource<12502>(), 12502)
''')
    resources = {}
    gen_predetermined_ids.ReadResourceIdsFromFile(f, resources)
    self.assertEqual(
        {
            12500: 'IDS_BOOKMARKS_NO_ITEMS',
            12501: 'IDS_BOOKMARK_BAR_IMPORT_LINK',
            12502: 'IDS_BOOKMARK_X'
        }, resources)

if __name__ == '__main__':
  unittest.main()
