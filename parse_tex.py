#!/usr/bin/env python

# Hung-Hsuan Chen <hhchen@psu.edu>
# Creation Date : 06-30-2013
# Last Modified: Mon 01 Jul 2013 09:32:35 PM EDT

import os
import sys

def parse_tex_abstract(filename):
  if not os.path.isfile(filename):
    raise Exception("Invalid file name %s" % (filename))

  is_in_abstract = False
  abs_contents = ''
  with open(filename) as f:
    for line in f:
      line = line.strip()
      if line[:6] == '\\begin' and line[line.find('{')+1:line.rfind('}')].strip() == 'abstract':
        is_in_abstract = True
      if is_in_abstract:
        abs_contents += ' '
        abs_contents += line
      if line[:4] == '\\end' and line[line.find('{')+1:line.rfind('}')].strip() == 'abstract':
        break
  return abs_contents[abs_contents.find('}') + 1 : abs_contents.find('\\end')].strip()

def main(argv):
  pass

if __name__ == "__main__":
  main(sys.argv)

from nose.tools import assert_equal

class TestAll():
  def test_parse_tex_abstract(self):
    tex_file = './test_tex_files/collabseer.tex'
    real_abs = '''Collaborative research has been increasingly popular and important in academic circles. However, there is no open platform available for scholars or scientists to effectively discover potential collaborators. This paper discusses CollabSeer, an open system to recommend potential research collaborators for scholars and scientists. CollabSeer discovers collaborators based on the structure of the coauthor network and a user's research interests. Currently, three different network structure analysis methods that use vertex similarity are supported in CollabSeer: Jaccard similarity, cosine similarity, and our relation strength similarity measure. Users can also request a recommendation by selecting a topic of interest. The topic of interest list is determined by CollabSeer's lexical analysis module, which analyzes the key phrases of previous publications. The CollabSeer system is highly modularized making it easy to add or replace the network analysis module or users' topic of interest analysis module. CollabSeer integrates the results of the two modules to recommend collaborators to users. Initial experimental results over the a subset of the CiteSeerX database shows that CollabSeer can efficiently  discover prospective collaborators.'''
    assert_equal(parse_tex_abstract(tex_file), real_abs)
