#!/usr/bin/env python

# Hung-Hsuan Chen <hhchen@psu.edu>
# Creation Date : 07-01-2013
# Last Modified: Tue 02 Jul 2013 11:12:55 PM EDT

import collections
import os
import sys

import gflags
import pytagcloud
import pytagcloud.lang.counter

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

def gen_tag_cloud(all_terms):
  # TODO: although pygame library looks like that it has beein successfully installed,
  #       import pygame.font raises exception...
  #       how to install pygame correctly?
  pytagcloud.create_tag_image(pytagcloud.lang.counter.get_tag_counts(all_terms),
      'cloud_large.png', size=(900, 600))

def dict_to_list_of_tuples(term_ctr):
  li_of_tup = [ ]
  for term in term_ctr:
    li_of_tup.append((term, term_ctr[term]))
  return li_of_tup

def main(argv):
  check_args(argv)

  all_terms = collections.defaultdict(int)
  tex_files = get_tex_files(FLAGS.tex_folder)
  for f in tex_files:
    abs = parse_tex.parse_tex_abstract(f)
    terms = get_nouns.get_nouns_and_noun_phrases(abs)
    for t in terms:
      term = ' '.join(t)
      #for i in range(2 * len(term.split())):  # repeat 2*n times for a n-gram
      all_terms[term] += 2 * len(term.split())  # the weight of an n-gram is set to 2 * n

  gen_tag_cloud(dict_to_list_of_tuples(all_terms))

if __name__ == "__main__":
  main(sys.argv)

from nose.tools import assert_equal, assert_true

class TestAll():
  def test_get_tex_files(self):
    tex_files = get_tex_files('./test_tex_files')
    assert_true(len(tex_files) > 0)
    for filename in tex_files:
      assert_equal(os.path.splitext(filename)[1], '.tex')
