#!/usr/bin/python3
# Copyright 2016 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Merge package entries from different package lists.
"""

# This is used for replacing packages in eg. bullseye with those in bookworm.
# The updated packages are ABI compatible, but include security patches, so we
# should use those instead in our sysroots.

import sys

if len(sys.argv) != 2:
  exit(1)

packages = {}

def AddPackagesFromFile(file):
  global packages
  lines = file.readlines()
  if len(lines) % 3 != 0:
    exit(1)
  for i in range(0, len(lines), 3):
    packages[lines[i]] = (lines[i + 1], lines[i + 2])

AddPackagesFromFile(open(sys.argv[1], 'r'))
AddPackagesFromFile(sys.stdin)

output_file = open(sys.argv[1], 'w')

for (package, (filename, sha256)) in packages.items():
  output_file.write(package + filename + sha256)
