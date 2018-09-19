# -*- coding: utf-8 -*-
"""
  disc1_base.py generated by WhatsOpt. 
"""
# DO NOT EDIT unless you know what you are doing
# analysis_id: 109

import numpy as np
from openmdao.api import ExplicitComponent

class Disc1Base(ExplicitComponent):
    """ An OpenMDAO base component to encapsulate Disc1 discipline """

    
    def setup(self):
		
        self.add_input('y2', val=1.0, desc='')
        self.add_input('x', val=1.0, desc='')
        self.add_input('z', val=np.ones((2,)), desc='')
		
        self.add_output('y1', val=1.0, desc='')
	

        