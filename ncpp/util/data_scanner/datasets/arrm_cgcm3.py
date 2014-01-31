import base
import abc


class AbstractARRM_CGCM3Dataset(base.AbstractFolderHarvestDataset):
    __metaclass__ = abc.ABCMeta
    folder = '/data/downscaled/arrm'
    dataset_category = dict(name='Downscaled',description='<tdk>')
    dataset = dict(name='Asynchronous Regional Regression Model CGCM3',description='<tdk>')
    type = 'variable'
    time_calendar = '365_day'
    
    
class ARRM_CGCM3Tasmin(AbstractARRM_CGCM3Dataset):
    _uri = 'arrm_cgcm3_t63.20c3m.tasmin.NAm.1971-2000.nc'
    variables = ['tasmin']
    clean_variable = [base.VAR_AIR_TEMPERATURE_MIN]
    clean_units = [base.UNITS_CELSIUS]
    
    
class ARRM_CGCM3Tas(AbstractARRM_CGCM3Dataset):
    _uri = 'arrm_cgcm3_t63.20c3m.tas.NAm.1971-2000.nc'
    variables = ['tas']
    clean_variable = [base.VAR_AIR_TEMPERATURE]
    clean_units = [base.UNITS_CELSIUS]


class ARRM_CGCM3Tasmax(AbstractARRM_CGCM3Dataset):
    _uri = 'arrm_cgcm3_t63.20c3m.tasmax.NAm.1971-2000.nc'
    variables = ['tasmax']
    clean_variable = [base.VAR_AIR_TEMPERATURE_MAX]
    clean_units = [base.UNITS_CELSIUS]
    
    
class ARRM_CGCM3Pr(AbstractARRM_CGCM3Dataset):
    _uri = 'arrm_cgcm3_t63.20c3m.pr.NAm.1971-2000.nc'
    variables = ['pr']
    clean_variable = [base.VAR_PRECIPITATION]
    clean_units = [base.UNITS_MM_PER_DAY]
