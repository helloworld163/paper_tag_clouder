#!/usr/bin/env python

# Hung-Hsuan Chen <hhchen@psu.edu>
# Creation Date : 07-01-2013
# Last Modified: Thu 04 Jul 2013 04:41:31 PM EDT

import collections
import operator
import os
import sys

import gflags

import parse_tex
import get_nouns

FLAGS = gflags.FLAGS
gflags.DEFINE_string('tex_folder', '', '')

def usage(cmd):
  print 'Usage:', cmd, \
        '--tex_folder="PATH/TO/TEX/DIR"'
  return

def check_args(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError:
    print FLAGS

  if not os.path.isdir(FLAGS.tex_folder):
    usage(argv[0])
    raise Exception('flag --tex_folder is not a valid directory')

def get_tex_files(folder_name):
  if not os.path.isdir(folder_name):
    raise Exception("Invalid folder name %s" % (folder_name))

  tex_files = [ ]
  file_names = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
  for filename in file_names:
    if os.path.splitext(filename)[1] == '.tex':
      tex_files.append(os.path.join(folder_name, filename))
  return tex_files

def gen_tag_cloud(term_ctr):
  with open('./d3-cloud/examples/word_ctr.txt', 'w') as f:
    for (term, freq) in term_ctr:
      f.write("%s:%d\n" % (term, int(round(freq))))

def sort_dict_by_value(x):
  return sorted(x.iteritems(), key=operator.itemgetter(1), reverse = True)

def main(argv):
  check_args(argv)

  all_terms = collections.defaultdict(int)
  tex_files = get_tex_files(FLAGS.tex_folder)
  for f in tex_files:
    abs = parse_tex.parse_tex_abstract(f)
    terms = get_nouns.get_nouns_and_noun_phrases(abs)
    for t in terms:
      term = ' '.join(t)
      if term != '':
        all_terms[term] += 2 * len(term.split())  # the weight of an n-gram is set to 2 * n

  gen_tag_cloud(sort_dict_by_value(all_terms))

if __name__ == "__main__":
  main(sys.argv)

from nose.tools import assert_equal, assert_true

class TestAll():
  def test_get_tex_files(self):
    tex_files = get_tex_files('./test_tex_files')
    assert_true(len(tex_files) > 0)
    for filename in tex_files:
      assert_equal(os.path.splitext(filename)[1], '.tex')
