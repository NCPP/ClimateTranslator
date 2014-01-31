import base
import maurer
import hayhoe
import arrm_cgcm3
import bcca_cccma_cgcm3
import bcca_gfdl_cm2_1


class MaurerPackage(base.AbstractDataPackage):
    name = 'Maurer 2010'
    description = '<tdk>'
    fields = [maurer.MaurerTas,
              maurer.MaurerTasmax,
              maurer.MaurerTasmin,
              maurer.MaurerPrecip]
    dataset_category = base.CATEGORY_GRIDDED_OBS
    
    
class HayhoeGFDLPackage(base.AbstractDataPackage):
    name = 'Asynchronous Regional Regression Model GFDL-CM2.1'
    description = '<tdk>'
    fields = [hayhoe.HayhoeGFDLPr,
              hayhoe.HayhoeGFDLTasmax,
              hayhoe.HayhoeGFDLTas,
              hayhoe.HayhoeGFDLTasmin]
    dataset_category = dict(name='Downscaled',description='<tdk>')
    
    
class ARRM_CGCM3Package(base.AbstractDataPackage):
    name = 'Asynchronous Regional Regression Model CGCM3'
    description = '<tdk>'
    fields = [arrm_cgcm3.ARRM_CGCM3Pr,
              arrm_cgcm3.ARRM_CGCM3Tas,
              arrm_cgcm3.ARRM_CGCM3Tasmax,
              arrm_cgcm3.ARRM_CGCM3Tasmin]
    dataset_category = dict(name='Downscaled',description='<tdk>')
    
    
class BCCA_CCCMA_CGCM3Package(base.AbstractDataPackage):
    name = 'Bias-Correction Constructed Analogs CGCM3'
    description = '<tdk>'
    fields = [bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Pr,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tas,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tasmax,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tasmin]
    dataset_category = dict(name='Downscaled',description='<tdk>')
    
    
class BCCA_GFDL_CM2_1Package(base.AbstractDataPackage):
    name = 'Bias-Correction Constructed Analogs GFDL-CM2.1'
    description = '<tdk>'
    fields = [bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Pr,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tas,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tasmin,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tasmax,]
    dataset_category = dict(name='Downscaled',description='<tdk>')


class DownscaledPrecipitation(base.AbstractDataPackage):
    _exclude = True
    name = 'Downscaled & Observational Precipitation'
    description = '<tdk>'
    fields = [maurer.MaurerPrecip,
              hayhoe.HayhoeGFDLPr,
              arrm_cgcm3.ARRM_CGCM3Pr,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Pr,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Pr]
    dataset_category = dict(name='Downscaled & Observational',description='<tdk>')


class DownscaledTas(base.AbstractDataPackage):
    _exclude = True
    name = 'Downscaled & Observational Air Temperature'
    description = '<tdk>'
    fields = [maurer.MaurerTas,
              hayhoe.HayhoeGFDLTas,
              arrm_cgcm3.ARRM_CGCM3Tas,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tas,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tas]
    dataset_category = dict(name='Downscaled & Observational',description='<tdk>')
    
    
class DownscaledTasmin(base.AbstractDataPackage):
    _exclude = True
    name = 'Downscaled & Observational Minimum Air Temperature'
    description = '<tdk>'
    fields = [maurer.MaurerTasmin,
              hayhoe.HayhoeGFDLTasmin,
              arrm_cgcm3.ARRM_CGCM3Tasmin,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tasmin,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tasmin]
    dataset_category = dict(name='Downscaled & Observational',description='<tdk>')
    
    
class DownscaledTasmax(base.AbstractDataPackage):
    _exclude = True
    name = 'Downscaled & Observational Maximum Air Temperature'
    description = '<tdk>'
    fields = [maurer.MaurerTasmax,
              hayhoe.HayhoeGFDLTasmax,
              arrm_cgcm3.ARRM_CGCM3Tasmax,
              bcca_cccma_cgcm3.BCCA_CCCMA_CGCM3Tasmax,
              bcca_gfdl_cm2_1.BCCA_GFDL_CM_2_1Tasmax]
    dataset_category = dict(name='Downscaled & Observational',description='<tdk>')
    
