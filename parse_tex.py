#!/usr/bin/env python

# Hung-Hsuan Chen <hhchen@psu.edu>
# Creation Date : 06-30-2013
# Last Modified: Sun 30 Jun 2013 11:08:06 PM EDT

import os
import sys

def get_tex_files(folder_name):
  if not os.path.isdir(folder_name):
    raise Exception("Invalid folder name %s" % (folder_name))

  tex_files = [ ]
  file_names = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
  for filename in file_names:
    if os.path.splitext(filename)[1] == '.tex':
      tex_files.append(os.path.join(folder_name, filename))
  return tex_files


def main(argv):
  pass

if __name__ == "__main__":
  main(sys.argv)

from nose.tools import assert_equal, assert_true

class TestAll():
  def test_get_tex_files(self):
    tex_files = get_tex_files('./test_tex_files')
    assert_true(len(tex_files) > 0)
    for filename in tex_files:
      assert_equal(os.path.splitext(filename)[1], '.tex')


