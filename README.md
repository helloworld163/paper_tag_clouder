paper_tag_clouder
=================

Author: Hung-Hsuan Chen (hhchen@psu.edu)

### Overview

The program takes tex files in the same folder as input, and extract the phrases
in the abstract paragraphs.  Based on the frequency of these phrases, the system
automatically generates tag cloud images.

### Sample generated tag clouds

Check out my website to see tag cloud images generated based on some of my
previous academic publications.

http://php.scripts.psu.edu/hxc249/misc.php

### Sample usage

$ ./main.py --tex_folder=PATH/TO/THE/FOLDER/CONTAINING/TEX/FILES

Open Google Chrome browser and go to
http://your.host.name/paper_tag_clouder/d3-cloud/examples/simple.html

You should see the generated tag cloud.

### Know issues

* Google Chrome 27.0.1453.116 can successfully render the generated tag cloud,
but Microsoft Internet Explorer 10 and Mozilla Firefox 22 cannnot render the
image.
