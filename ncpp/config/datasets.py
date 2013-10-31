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

    def getDatasets(self, data_type, variable=None, time_frequency=None, dataset_category=None, dataset=None):
        
        '''dict = 
           {'long_name': [u'Air Temperature', u'Daily Precipitation Rate', u'Maximum Air Temperature', u'Minimum Air Temperature'], 
            'time_frequency': [u'day'], 'dataset_category': [u'Downscaled', u'Gridded Observational'], 
            'dataset': [u'Hayhoe ARRM-GFDL', u'Maurer 2010']}
        '''
        
        if data_type=='variable':
            dict = self.dataQuery.get_variable_or_index('variable', long_name=variable, time_frequency=time_frequency, 
                                                        dataset_category=dataset_category, dataset=dataset)
            print 'Dataset options: %s' % dict
            return dict
        
        else:
            raise Exception('Unsupported data type=%s' % data_type)
    
    def getTimeFrequencies(self, long_name):
        print 'query for time frequencies for long_name=%s' % long_name
        
        # FIXME
        dict = self.dataQuery.get_variable_or_index('variable')
        #dict = self.dataQuery.get_variable_or_index('variable', long_name=long_name)
        print 'frequencies=%s' % dict
        tuples = [] 
        for value in dict['time_frequency']:
            tuples.append( (str(value), str(value)) )
        return sorted(tuples, key=lambda t: t[1])
    
        
        
ocgisDatasets = DbDatasets(DATASETS_DB) 
        