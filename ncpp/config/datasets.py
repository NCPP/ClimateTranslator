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
        
        return tuples

    def getDatasets(self, data_type, long_name=None, time_frequency=None, dataset_category=None, dataset=None,
                                     dataset_category2=None, package_name=None):
        
        '''dict = 
           {'long_name': [u'Air Temperature', u'Daily Precipitation Rate', u'Maximum Air Temperature', u'Minimum Air Temperature'], 
            'time_frequency': [u'day'], 'dataset_category': [u'Downscaled', u'Gridded Observational'], 
            'dataset': [u'Hayhoe ARRM-GFDL', u'Maurer 2010']}
        '''
        
        if data_type=='variable':
            dict = self.dataQuery.get_variable_or_index('variable', long_name=long_name, time_frequency=time_frequency, 
                                                        dataset_category=dataset_category, dataset=dataset)        
        elif data_type=='package':
            
            dict = self.dataQuery.get_package(dataset_category=dataset_category2, package_name=package_name)
                                                    
        else:
            raise Exception('Unsupported data type=%s' % data_type)
        
        return dict
    
    # FIXME ?
    def get_variable_or_index_dataset(self, data_type, long_name=None, time_frequency=None, 
                                            dataset_category=None, dataset=None):
        
        if data_type=='variable':
            dictionaries = self.dataQuery.get_variable_or_index_dataset('variable', long_name=long_name, time_frequency=time_frequency, 
                                                                            dataset_category=dataset_category, dataset=dataset)  
            return dictionaries
        else:
            raise Exception("data_type=index not yet implemented")
        
    def get_package_datasets(self, package_name=None):
        
        dictionaries = self.dataQuery.get_package_datasets(package_name=package_name)
        return dictionaries
        
ocgisDatasets = DbDatasets(DATASETS_DB) 
        