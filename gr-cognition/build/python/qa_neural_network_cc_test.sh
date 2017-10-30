#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/ljwong/digicom/gr-cognition/python
export PATH=/home/ljwong/digicom/gr-cognition/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/ljwong/digicom/gr-cognition/build/swig:$PYTHONPATH
/usr/bin/python2 /home/ljwong/digicom/gr-cognition/python/qa_neural_network_cc.py 
