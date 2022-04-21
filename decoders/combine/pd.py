##
## This file is part of the libsigrokdecode project.
##
## 
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd

class Decoder(srd.Decoder):
    api_version = 3
    id = 'combine'
    name = 'Combine'
    longname = 'combine channels'
    desc = 'Combine different channels.'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = []
    tags = [ 'Util']
    channels = (
        {'id': 'd0', 'name': 'D0', 'desc': 'Data 0 line'},
        {'id': 'd1', 'name': 'D1', 'desc': 'Data 1 line'},
    )
    options = (
        {'id': 'logic_function', 'desc': 'Logic function to apply',
         'default': 'or', 'values': ('and', 'or', 'xor')},
    )
    annotations = (
        ('bit', 'Bit'),
    )
    annotation_rows = (
        ('bits', 'Bits', (0,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.d0_prev = None
        self.d1_prev = None
        self.initialized = False 

        self.sample_prev = 0

    def start(self):
        'Register output types and verify user supplied decoder values.'
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def metadata(self, key, value):
        'Receive decoder metadata about the data stream.'
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value
    
    def combine(self):
        if self.options['logic_function'] == 'and':
            return self.d0_prev & self.d1_prev
        elif self.options['logic_function']== 'or': 
            return self.d0_prev | self.d1_prev
        else:
            return self.d0_prev ^ self.d1_prev

    def decode(self):
        while True:
            
            cond=[]
            if (self.initialized):
                # wait for a state change on either channel
                cond=[{0: 'e'}, {1: 'e'}]
                
            (d0, d1) = self.wait(cond)
            
            if (self.initialized):
                self.put(self.sample_prev, self.samplenum, self.out_ann,
                     [0,[str(self.combine())]])
            
            self.sample_prev=self.samplenum
            (self.d0_prev, self.d1_prev)=(d0,d1)
            self.initialized = True

    def report(self):
        return '%s: OK' % self.name
