import abc
from ncpp.util.data_scanner.query import DataQuery
from ncpp.constants import DATASETS_DB, NO_VALUE_OPTION

VARIABLE = 'variable'
PACKAGE = 'package'

# FIXME
#db_path = '/Users/cinquini/Documents/workspace-cog/ClimateTranslator/database/datasets.sqlite'

class Datasets(object):
    '''Abstract API for accessing Datasets configuration in Climate Translator application.'''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        pass
    
class DbDatasets(Datasets):
    '''Implementation of Datasets API that retrieves information from a database back-end.'''
    
    def __init__(self, db_path):
        self.dataQuery = DataQuery(db_path=db_path)
        
    def getDataTypes(self):
        # no option selected
        tuples = [ NO_VALUE_OPTION ]
        tuples.append( (VARIABLE, VARIABLE.capitalize()) ) # (key, label)
        tuples.append( (PACKAGE, PACKAGE.capitalize()) )   # (key, label)
        
        # read all keys from JSON file
        #for category in sorted( self.datasets.keys() ):
        #    tuples.append( (category, category) )
        return tuples

    def getVariables(self):
        
        '''dict = 
           {'long_name': [u'Air Temperature', u'Daily Precipitation Rate', u'Maximum Air Temperature', u'Minimum Air Temperature'], 
            'time_frequency': [u'day'], 'dataset_category': [u'Downscaled', u'Gridded Observational'], 
            'dataset': [u'Hayhoe ARRM-GFDL', u'Maurer 2010']}
        '''
        print 'querying for variables'
        dict = self.dataQuery.get_variable_or_index('variable')
        print dict
        tuples = []
        for value in dict['long_name']:
            tuples.append( (str(value), str(value)) )
        return sorted(tuples, key=lambda t: t[1])
        
        
ocgisDatasets = DbDatasets(DATASETS_DB) 
        