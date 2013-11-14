import base
import abc


class AbstractBCCA_GFDL_CM_2_1(base.AbstractFolderHarvestDataset):
    __metaclass__ = abc.ABCMeta
    folder = '/data/downscaled/bcca'
    dataset_category = dict(name='Downscaled',description='<tdk>')
    dataset = dict(name='BCCA-GFDL-CM2.1',description='<tdk>')
    type = 'variable'
    
    
class BCCA_GFDL_CM_2_1Tasmin(AbstractBCCA_GFDL_CM_2_1):
    _uri = 'bcca_gfdl_cm2_1.gregorian.20c3m.run1.tasmin.1971-2000.nc'
    variables = ['tasmin']
    clean_variable = [base.VAR_AIR_TEMPERATURE_MIN]
    clean_units = [base.UNITS_CELSIUS]
    
    
class BCCA_GFDL_CM_2_1Tas(AbstractBCCA_GFDL_CM_2_1):
    _uri = 'bcca_gfdl_cm2_1.gregorian.20c3m.run1.tas.1971-2000.nc'
    variables = ['tas']
    clean_variable = [base.VAR_AIR_TEMPERATURE]
    clean_units = [base.UNITS_CELSIUS]


class BCCA_GFDL_CM_2_1Tasmax(AbstractBCCA_GFDL_CM_2_1):
    _uri = 'bcca_gfdl_cm2_1.gregorian.20c3m.run1.tasmax.1971-2000.nc'
    variables = ['tasmax']
    clean_variable = [base.VAR_AIR_TEMPERATURE_MAX]
    clean_units = [base.UNITS_CELSIUS]
    
    
class BCCA_GFDL_CM_2_1Pr(AbstractBCCA_GFDL_CM_2_1):
    _uri = 'bcca_gfdl_cm2_1.gregorian.20c3m.run1.pr.1971-2000.nc'
    variables = ['pr']
    clean_variable = [base.VAR_PRECIPITATION]
    clean_units = [base.UNITS_MM_PER_DAY]
