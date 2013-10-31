import abc

from ncpp.constants import GEOMETRIES_FILEPATH, NO_VALUE_OPTION
import json

class Geometries(object):
    """API for accessing geometries within Climate Translator application."""
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def getCategories(self):
        return []
    
    @abc.abstractmethod
    def getSubCategories(self, category):
        return []
    
    @abc.abstractmethod
    def getGeometries(self, category, subcategory):
        return []
    
    @abc.abstractmethod
    def getGuid(self, category, subcategory, geometry):
        return ""
    
    @abc.abstractmethod
    def getCategoryKey(self, category):
        return ""

class JsonGeometries(Geometries):
    """Class that reads supported geometries from a JSON file."""
    
    def __init__(self, filepath):
        
        # read geometries from JSON file
        try:
            with open(filepath,'r') as f:
                self.geometries = json.load(f)
        except Exception as e:
            print "Error reading geometry file: %s" % GEOMETRIES_FILEPATH
            raise e
        
    def getCategories(self):
        # no option selected
        tuples = [ NO_VALUE_OPTION ]
        # first option is US States
        tuples.append( ('US State Boundaries', 'US State Boundaries') )
        # then all US counties
        for category in sorted( self.geometries.keys() ):
            if category != 'US State Boundaries':
                tuples.append( (category, category) )
        return tuples
    
    def getSubCategories(self, category):
        
        subcategories = self.geometries[category]['geometries']
        print 'subcats=%s' % subcategories
        
        # multiple sub-categories
        if len(subcategories)>1:                   
            tuples = [ (NO_VALUE_OPTION[1], NO_VALUE_OPTION[0]) ] # no option selected
            for k,v in subcategories.items():
                tuples.append( (k,k) )       
                
        # only one sub-category     
        else:
            tuples = []
            for k,v in subcategories.items():
                tuples.append( ("-- No Selection Required --", k) )            
          
        return sorted(tuples, key=lambda t: t[1])
    
    def getGeometries(self, category, subcategory):
        
        tuples = []
        for k,v in self.geometries[category]['geometries'][subcategory].items():
            tuples.append( (k,k) )
        return sorted(tuples, key=lambda t: t[1])
    
    def getGuid(self, category, subcategory, geometry):
        return self.geometries[category]['geometries'][subcategory][geometry]
    
    def getCategoryKey(self, category):
        return self.geometries[category]['key']

ocgisGeometries = JsonGeometries(GEOMETRIES_FILEPATH)     