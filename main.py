#!/usr/bin/env python

# Hung-Hsuan Chen <hhchen@psu.edu>
# Creation Date : 07-01-2013
# Last Modified: Wed 03 Jul 2013 09:53:42 PM EDT

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
  # TODO: maybe use one of the following options instead?
  #       1. http://peekaboo-vision.blogspot.com/2012/11/a-wordcloud-in-python.html and 
  #          https://github.com/amueller/word_cloud
  #       2. https://github.com/jasondavies/d3-cloud
  #       3. https://github.com/indyarmy/jQuery.awesomeCloud.plugin
  with open('./d3-cloud/examples/word_ctr.txt', 'w') as f:
    for (term, freq) in term_ctr:
      f.write("%s:%d\n" % (term, int(round(freq))))

def sort_dict_by_value(x):
  return sorted(x.iteritems(), key=operator.itemgetter(1), reverse = True)

def normalize_ctr_values(all_terms, new_min, new_max):
  orig_max = max(all_terms.values())
  orig_min = min(all_terms.values())
  for term in all_terms:
    all_terms[term] = new_min + \
        float(new_max - new_min) * (all_terms[term] - orig_min) / (orig_max - orig_min)

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

  normalize_ctr_values(all_terms, 10, 100)
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
