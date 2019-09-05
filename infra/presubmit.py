#!/usr/bin/env python
# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
"""Statically check project for common issues."""

from __future__ import print_function

import os
import sys


def get_oss_fuzz_root():
  """Get the absolute path of the root of the oss-fuzz checkout."""
  script_path = os.path.realpath(__file__)
  return os.path.abspath(os.path.join(os.path.dirname(script_path), '..'))


def check_lib_fuzzing_engine(project_path):
  build_sh_path = os.path.join(project_path, 'build.sh')
  if not os.path.exists(build_sh_path):
    return True

  with open(build_sh_path) as build_sh:
    build_sh_lines = build_sh.readlines()
  for line_num, line in enumerate(build_sh_lines):
    uncommented_code = line.split('#')[0]
    if '-lFuzzingEngine' in uncommented_code:
      print('build.sh contains -lFuzzingEngine on line:', line_num)
      return False
  return True


def check_project_yaml(project_path):
  # TODO(metzman): Check that valid emails are used, a homepage is specified,
  # ensure valid yaml and complain about omittable configs, ie:
  # architectures:
  # - x86_64
  return True


def check_project(project):
  oss_fuzz_root = get_oss_fuzz_root()
  project_path = os.path.join(oss_fuzz_root, 'projects', project)
  success = True
  checks = [check_project_yaml, check_lib_fuzzing_engine]
  for check in checks:
    result = check(project_path)
    success = result if success else success
  return success


def main():
  if len(sys.argv) != 2:
    print('Usage: {0} <project>'.format(sys.argv[0]))
  if not check_project(sys.argv[1]):
    exit(1)

if __name__ == '__main__':
  main()
