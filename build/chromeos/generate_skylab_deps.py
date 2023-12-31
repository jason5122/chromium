#!/usr/bin/python3
#
# Copyright 2022 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import json
import os
import re
import sys

# The basic shell script for client test run in Skylab. The arguments listed
# here will be fed by autotest at the run time.
#
# * test-launcher-summary-output: the path for the json result. It will be
#     assigned by autotest, who will upload it to GCS upon test completion.
# * test-launcher-shard-index: the index for this test run.
# * test-launcher-total-shards: the total test shards.
# * test_args: arbitrary runtime arguments configured in test_suites.pyl,
#     attached after '--'.
BASIC_SHELL_SCRIPT = """
#!/bin/sh

while [[ $# -gt 0 ]]; do
    case "$1" in
        --test-launcher-summary-output)
            summary_output=$2
            shift 2
            ;;

        --test-launcher-shard-index)
            shard_index=$2
            shift 2
            ;;

        --test-launcher-total-shards)
            total_shards=$2
            shift 2
            ;;

        --)
            test_args=$2
            break
            ;;

        *)
            break
            ;;
    esac
done

if [ ! -d $(dirname $summary_output) ] ; then
    mkdir -p $(dirname $summary_output)
fi

cd `dirname $0` && cd ..
"""


def build_test_script(args):
  # Build the shell script that will be used on the device to invoke the test.
  # Stored here as a list of lines.
  device_test_script_contents = BASIC_SHELL_SCRIPT.split('\n')

  test_invocation = ('LD_LIBRARY_PATH=./ ./%s '
                     ' --test-launcher-summary-output=$summary_output'
                     ' --test-launcher-shard-index=$shard_index'
                     ' --test-launcher-total-shards=$total_shards'
                     ' $test_args' % args.test_exe)

  device_test_script_contents.append(test_invocation)
  with open(args.output, 'w') as w:
    w.write('\n'.join(device_test_script_contents))
  os.chmod(args.output, 0o755)


def build_filter_file(args):
  # TODO(b/227381644): This expression is hard to follow and  should be
  # simplified. This would require a change on the cros infra side as well
  tast_expr_dict = {}
  default_disabled_tests = []
  if args.disabled_tests is not None:
    default_disabled_tests = [
        '!"name:{0}"'.format(test) for test in args.disabled_tests
    ]

  default_enabled_test_term = ''
  if args.enabled_tests is not None:
    default_enabled_test_term = (' || ').join(
        ['"name:{0}"'.format(test) for test in args.enabled_tests])

  # Generate the default expression to be used when there is no known key
  tast_expr = args.tast_expr if args.tast_expr else ""

  if default_disabled_tests:
    default_disabled_term = " && ".join(default_disabled_tests)
    tast_expr = "{0} && {1}".format(tast_expr, default_disabled_term) if \
      tast_expr else default_disabled_term

  if default_enabled_test_term:
    tast_expr = "{0} && ({1})".format(
        tast_expr,
        default_enabled_test_term) if tast_expr else default_enabled_test_term

  tast_expr_dict['default'] = "({0})".format(tast_expr)

  # Generate an expression for each collection in the gni file
  if args.tast_control is not None:
    with open(args.tast_control, 'r') as tast_control_file:
      gni = tast_control_file.read()
      filter_lists = re.findall(r'(.*) = \[([^\]]*)\]', gni)
      for filter_list in filter_lists:
        tast_expr = args.tast_expr if args.tast_expr else ""

        milestone_disabled_tests = {
            '!"name:{0}"'.format(test)
            for test in re.findall(r'"([^"]+)"', filter_list[1])
        }

        milestone_disabled_tests.update(default_disabled_tests)

        if milestone_disabled_tests:
          tast_expr = "{0} && {1}".format(
              tast_expr, " && ".join(milestone_disabled_tests)
          ) if tast_expr else " && ".join(milestone_disabled_tests)

        if default_enabled_test_term:
          tast_expr = "{0} && ({1})".format(
              tast_expr, default_enabled_test_term
          ) if tast_expr else default_enabled_test_term

        if tast_expr:
          tast_expr_dict[filter_list[0]] = "({0})".format(tast_expr)

  if len(tast_expr_dict) > 0:
    with open(args.output, "w") as file:
      json.dump(tast_expr_dict, file, indent=2)
    os.chmod(args.output, 0o644)


def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(dest='command')

  script_gen_parser = subparsers.add_parser('generate-runner')
  script_gen_parser.add_argument(
      '--test-exe',
      type=str,
      required=True,
      help='Path to test executable to run inside the device.')
  script_gen_parser.add_argument('--verbose', '-v', action='store_true')
  script_gen_parser.add_argument(
      '--output',
      required=True,
      type=str,
      help='Path to create the runner script.')
  script_gen_parser.set_defaults(func=build_test_script)

  filter_gen_parser = subparsers.add_parser('generate-filter')
  filter_gen_parser.add_argument(
      '--tast-expr',
      type=str,
      required=False,
      help='Tast expression to determine tests to run. This creates the '
      'initial set of tests that can be further filtered.')
  filter_gen_parser.add_argument(
      '--enabled-tests',
      type=str,
      required=False,
      action='append',
      help='Name of tests to allow to test (unnamed tests will not run).')
  filter_gen_parser.add_argument(
      '--disabled-tests',
      type=str,
      required=False,
      action='append',
      help='Names of tests to disable from running')
  filter_gen_parser.add_argument(
      '--tast-control',
      type=str,
      required=False,
      help='Filename for the tast_control file containing version skew '
      'test filters to generate.')
  filter_gen_parser.add_argument(
      '--output',
      required=True,
      type=str,
      help='Path to create the plain text filter file.')
  filter_gen_parser.set_defaults(func=build_filter_file)

  args = parser.parse_args()

  if (args.command == "generate-filter" and args.disabled_tests is None and
      args.enabled_tests is None and args.tast_expr is None):
    parser.error(
        '--disabled-tests, --enabled-tests, or --tast-expr must be provided '
        'to generate-filter')

  args.func(args)

  return 0


if __name__ == '__main__':
  sys.exit(main())
