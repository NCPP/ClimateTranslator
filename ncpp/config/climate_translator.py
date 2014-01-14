# module containing configuration classes for Open Climate GIS application
from ncpp.constants import CONFIG_FILEPATH, GEOMETRIES_FILEPATH, CALCULATIONS_FILEPATH, NO_VALUE_OPTION, NO_VALUE_OPTION2
import json
import os, ConfigParser
import abc
from collections import OrderedDict

class ConfigBase(object):
    """Abstract Base Class for Climate Translator configuration."""
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def getChoices(self):
        """Returns a list of choices for selection in the web interface.
           Each tuple has the form (choice value, choice label).""" 
        return []
    

ocgisConfig = ConfigParser.RawConfigParser(dict_type=OrderedDict)
#ocgisConfig = ConfigParser.RawConfigParser()
# must set following line explicitely to preserve the case of configuration keys
ocgisConfig.optionxform = str 
try:
    ocgisConfig.read( os.path.expanduser(CONFIG_FILEPATH) )
except Exception as e:
    print "Configuration file %s not found" % CONFIG_FILEPATH
    raise e

class Config():
    '''Class holding keys into configuration file.'''
    
    DEFAULT = 'default'
    VARIABLE = 'variable'
    OUTPUT_FORMAT = 'output_format'
    CALCULATION_GROUP = 'calculation_group'
    SPATIAL_OPERATION = 'spatial_operation'
    
    
def ocgisChoices(section, nochoice=False):
    choices = OrderedDict()
    # add empty choice 
    if nochoice:
        choices[ NO_VALUE_OPTION[0] ] = NO_VALUE_OPTION[1]
    # iterate over configuration choices in original order
    for key, value in ocgisConfig.items(section):
        choices[ key ] = value
    return choices

class Calculations(ConfigBase):
    """Class holding Climate Translator choices for calculations."""
    
    def __init__(self):
        # read calculations from JSON file
        try:
            with open(CALCULATIONS_FILEPATH,'r') as f:
                self.calcs = json.load(f)
        except Exception as e:
            print "Error reading calculations file: %s" % CALCULATIONS_FILEPATH
            raise e
            
    def getChoices(self):
        
        # no option selected
        choices = [ NO_VALUE_OPTION2 ]
        # then all US counties
        for key in sorted( self.calcs, key=lambda key: self.calcs[key]["order"] ):
            calc = self.calcs[key]
            choices.append( (key, calc["name"]) )
        return choices
    
    def getCalc(self, key):
        return self.calcs[key]
    
    def _print(self):
        for key in sorted( self.calcs, key=lambda key: self.calcs[key]["order"] ):
            print "calculation=%s" % self.calcs[key]
        
ocgisCalculations = Calculations()
