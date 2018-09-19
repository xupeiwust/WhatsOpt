# -*- coding: utf-8 -*-
"""
  sellar_conversions.py generated by WhatsOpt. 
"""
import numpy as np
from .sellar.ttypes import *


# Disc1 
def to_openmdao_disc1_inputs(ins, inputs={}):
    
    inputs['y2'] = np.array(ins.y2)
    inputs['x'] = np.array(ins.x)
    inputs['z'] = np.array(ins.z)
    return inputs

def to_thrift_disc1_input(inputs):
    ins = Disc1Input()
    
    
    ins.y2 = float(inputs['y2'])
    
    
    ins.x = float(inputs['x'])
    
    
    ins.z = inputs['z'].tolist()
    
    return ins

def to_openmdao_disc1_outputs(output, outputs={}):
    
    outputs['y1'] = np.array(output.y1)
    return outputs

def to_thrift_disc1_output(outputs):
    output = Disc1Output()
    
    
    output.y1 = float(outputs['y1'])
    
    return output

# Disc2 
def to_openmdao_disc2_inputs(ins, inputs={}):
    
    inputs['y1'] = np.array(ins.y1)
    inputs['z'] = np.array(ins.z)
    return inputs

def to_thrift_disc2_input(inputs):
    ins = Disc2Input()
    
    
    ins.y1 = float(inputs['y1'])
    
    
    ins.z = inputs['z'].tolist()
    
    return ins

def to_openmdao_disc2_outputs(output, outputs={}):
    
    outputs['y2'] = np.array(output.y2)
    return outputs

def to_thrift_disc2_output(outputs):
    output = Disc2Output()
    
    
    output.y2 = float(outputs['y2'])
    
    return output

# Functions 
def to_openmdao_functions_inputs(ins, inputs={}):
    
    inputs['z'] = np.array(ins.z)
    inputs['y1'] = np.array(ins.y1)
    inputs['y2'] = np.array(ins.y2)
    inputs['x'] = np.array(ins.x)
    return inputs

def to_thrift_functions_input(inputs):
    ins = FunctionsInput()
    
    
    ins.z = inputs['z'].tolist()
    
    
    ins.y1 = float(inputs['y1'])
    
    
    ins.y2 = float(inputs['y2'])
    
    
    ins.x = float(inputs['x'])
    
    return ins

def to_openmdao_functions_outputs(output, outputs={}):
    
    outputs['obj'] = np.array(output.obj)
    outputs['g1'] = np.array(output.g1)
    outputs['g2'] = np.array(output.g2)
    return outputs

def to_thrift_functions_output(outputs):
    output = FunctionsOutput()
    
    
    output.obj = float(outputs['obj'])
    
    
    output.g1 = float(outputs['g1'])
    
    
    output.g2 = float(outputs['g2'])
    
    return output

