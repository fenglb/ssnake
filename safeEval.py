#!/usr/bin/env python

# Copyright 2015 Bas van Meerten and Wouter Franssen

#This file is part of ssNake.
#
#ssNake is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ssNake is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ssNake. If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, QtCore
import math
import re
import numpy as np
from euro import euro

def safeEval(inp):
    env = vars(math).copy()
    env["locals"]   = None
    env["globals"]  = None
    env["__name__"] = None
    env["__file__"] = None
    env["__builtins__"] = None
    env["slice"] = slice
    inp =  re.sub('([0-9]+)[k,K]','\g<1>*1024',str(inp)) #WF: allow 'K' input
    try:
        return eval(inp,env)
    except:
        return None

class SliceValidator(QtGui.QValidator):    
    def validate(self, string, position):
        string = str(string)
        try:
            int(safeEval(string))
            return (QtGui.QValidator.Acceptable,string,position)
        except:
            return (QtGui.QValidator.Intermediate,string,position)

class SliceSpinBox(QtGui.QSpinBox):
    def __init__(self, parent,minimum,maximum,*args, **kwargs):
        self.validator = SliceValidator()
        QtGui.QDoubleSpinBox.__init__(self,parent,*args, **kwargs)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setKeyboardTracking(False)

    def validate(self, text, position):
        return self.validator.validate(text, position)

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        inp = int(safeEval(str(text)))
        if inp < 0:
            inp = inp + self.maximum() +1
        return inp

    def textFromValue(self, value):
        inp = int(value)
        if inp < 0:
            inp = inp + self.maximum() + 1
        return str(inp)

class QLabel(QtGui.QLabel):
    def __init__(self, parent,*args, **kwargs):
        QtGui.QLabel.__init__(self, parent,*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter)
