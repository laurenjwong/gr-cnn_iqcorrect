#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
from keras.optimizers import SGD
from keras.models import model_from_json
from keras.models import load_model
from keras import backend as K
from argparse import ArgumentParser
from keras.layers.convolutional import Convolution1D
import numpy as np
import time
from keras.utils.np_utils import to_categorical
import os

class neural_network_cc(gr.basic_block):
    """
    docstring for block neural_network_cc
    """

    def __init__(self):
        gr.basic_block.__init__(self,
            name="neural_network_cc",
            in_sig=[numpy.complex64,numpy.complex64],
            out_sig=[numpy.complex64])
        self.set_min_output_buffer(512)

        self.mag_model = load_model('./est_mag_QAM2048_normcont.h5')
        self.ph_model = load_model('./est_ph_QAM2048_normcont.h5')
        self.count = 0
        self.magSum = 0.0
        self.phSum = 0.0

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        ninput_items_required[0] = 1024
        ninput_items_required[1] = 512



    def general_work(self, input_items, output_items):
        if len(input_items[0]) < 1024 or len(input_items[1]) < 512 or len(output_items[0]) < 512:
            print ("WTF?????????")
            return 0

        self.count += 1
        theta = (0.0*numpy.pi)/180.0

        # <+signal processing here+>
        samples = input_items[0][0:1024:1]
        rrcosSamples = input_items[1][0:512:1]
        realSamps = samples.real
        imagSamps = samples.imag
        together = numpy.empty((realSamps.size + imagSamps.size), dtype=realSamps.dtype)
        together[0::2] = realSamps
        together[1::2] = imagSamps

        #together = np.vstack((realSamps, imagSamps))
        together = together.reshape(1,1,1024,2)

        oneMag = self.mag_model.predict(together)
        self.magSum += oneMag
        alpha = self.magSum/self.count
        #print "one gain estimate: " , oneMag
        #print "average gain estimage: ", alpha

        onePh = self.ph_model.predict(together)
        self.phSum += onePh
        theta = self.phSum/self.count
        #print "one phase estimate: " , onePh
        #print "average phase estimage: ", theta


        real = rrcosSamples.real
        imag = rrcosSamples.imag

        real1 = real * (1.0/((1.0+alpha)*numpy.cos(theta)))
        real2 = real * (-numpy.sin(theta)/numpy.cos(theta))
        imag = imag * -1.0
        imag = real2 + imag
        imag = imag * -1.0
        ans = real1+1.0j*imag

        output_items[0][0:512] = ans
        self.consume(0, 1024)
        self.consume(1, 512)

        return 512
