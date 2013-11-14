
from ncpp.util.data_scanner.query import DataQuery
from ncpp.constants import DATASETS_DB

dataQuery = DataQuery(db_path=DATASETS_DB)

data_type = 'variable'
long_name = 'Maximum Air Temperature'
time_frequency = 'Day'
dataset_category = 'Downscaled'
dataset = 'BCCA-CCCMA-CGCM3'

dictionaries = dataQuery.get_variable_or_index_dataset('variable', long_name=long_name, time_frequency=time_frequency, 
                                                                  dataset_category=dataset_category, dataset=dataset)  