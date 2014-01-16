from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponse
from django.contrib.auth.models import User

from ncpp.models.common import JOB_STATUS
from ncpp.models.climate_translator import OpenClimateGisJob
from ncpp.config.climate_translator import ocgisChoices, Config, ocgisConfig, ocgisCalculations
from ncpp.config.geometries import ocgisGeometries
from ncpp.config.datasets import ocgisDatasets, VARIABLE, PACKAGE
from ncpp.utils import get_full_class_name, str2bool, hasText, formatListForDisplay
from ncpp.utils import get_month_string
from django.utils import simplejson  
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from ncpp.constants import NO_VALUE_OPTION, DATETIME_FORMAT

from datetime import datetime
import json

class ClimateTranslatorWizard(SessionWizardView):
    '''Set of views to submit an Open Climate GIS request.'''
    
    template_name = "ncpp/climate_translator/wizard_form.html"

    # method called at every step after the form data has been validated, before rendering of the view
    # overridden here to aggregate user choices from all steps before the last one
    def get_context_data(self, form, **kwargs):
        
        context = super(ClimateTranslatorWizard, self).get_context_data(form=form, **kwargs)
                  
        # before rendering of first form: send data and geometry choices 
        if self.steps.current == self.steps.first:
            #context.update({'datasets':  json.dumps(ocgisDatasets.datasets) }) # FIXME ?
            context.update({'geometries':  json.dumps(ocgisGeometries.geometries) })
            
        elif self.steps.current == "1":  # note: string type
            context.update({'calculations':  json.dumps(ocgisCalculations.calcs) }) 
                
        # before very last view: create summary of user choices
        elif self.steps.current == self.steps.last:
            job_data = {}
            # retrieve form data for all previous views
            for step in self.steps.all:
                cleaned_data = self.get_cleaned_data_for_step(step) 
                
                # first form
                if step == '0':                
                    job_data['data_type'] = cleaned_data['data_type']  
                    if cleaned_data.has_key('long_name'):
                        job_data['long_name'] = cleaned_data['long_name']  
                    if cleaned_data.has_key('time_frequency'):
                        job_data['time_frequency'] = cleaned_data['time_frequency']                          
                    if cleaned_data.has_key("dataset_category"):
                        job_data['dataset_category'] = cleaned_data['dataset_category'] 
                    if cleaned_data.has_key("dataset"):
                        job_data['dataset'] = cleaned_data['dataset'] 
                    if cleaned_data.has_key("dataset_category2"):
                        job_data['dataset_category2'] = cleaned_data['dataset_category2'] 
                    if cleaned_data.has_key("package_name"):
                        job_data['package_name'] = cleaned_data['package_name']                         
                    if cleaned_data.has_key('geometry_category') and hasText(cleaned_data['geometry_category']):
                        job_data['geometry_category'] = cleaned_data['geometry_category']
                    if cleaned_data.has_key('geometry_subcategory') and hasText(cleaned_data['geometry_subcategory']):
                        job_data['geometry_subcategory'] = cleaned_data['geometry_subcategory']                        
                    if cleaned_data.has_key('geometry_id') and len( cleaned_data['geometry_id'] )>0:
                        job_data['geometry_id'] = formatListForDisplay(cleaned_data['geometry_id'])
                    if cleaned_data.has_key('latmin') and cleaned_data['latmin'] is not None:
                        job_data['latmin'] = float( cleaned_data['latmin'] )
                    if cleaned_data.has_key('latmax') and cleaned_data['latmax'] is not None:
                        job_data['latmax'] = float( cleaned_data['latmax'] )
                    if cleaned_data.has_key('lonmin') and cleaned_data['lonmin'] is not None:
                        job_data['lonmin'] = float( cleaned_data['lonmin'] )
                    if cleaned_data.has_key('lonmax') and cleaned_data['lonmax'] is not None:
                        job_data['lonmax'] = float( cleaned_data['lonmax'] )
                    if cleaned_data.has_key('lat') and cleaned_data['lat'] is not None:
                        job_data['lat'] = float( cleaned_data['lat'] )
                    if cleaned_data.has_key('lon') and cleaned_data['lon'] is not None:
                        job_data['lon'] = float( cleaned_data['lon'] )
                    if cleaned_data.has_key('agg_selection'):
                        job_data['agg_selection'] = bool(cleaned_data['agg_selection'])
                    if cleaned_data.has_key('spatial_operation'):
                        job_data['spatial_operation'] = ocgisChoices(Config.SPATIAL_OPERATION)[cleaned_data['spatial_operation']]
                    if cleaned_data.has_key('datetime_start') and cleaned_data['datetime_start'] is not None:
                        job_data['datetime_start'] = cleaned_data['datetime_start']
                    if cleaned_data.has_key('datetime_stop') and cleaned_data['datetime_stop'] is not None:
                        job_data['datetime_stop'] = cleaned_data['datetime_stop']
                    if cleaned_data.has_key('timeregion_month') and cleaned_data['timeregion_month'] is not None:
                        job_data['timeregion_month'] = get_month_string( cleaned_data['timeregion_month'] )
                    if cleaned_data.has_key('timeregion_year') and cleaned_data['timeregion_year'] is not None:
                        job_data['timeregion_year'] = cleaned_data['timeregion_year']
                 
                # second form       
                if step == '1':
                    if cleaned_data.has_key('calc') and cleaned_data['calc'] is not None and cleaned_data['calc'] != '':
                        job_data['calc'] = ocgisCalculations.getCalc(cleaned_data['calc'])["name"]             
                    if cleaned_data.has_key('par1') and cleaned_data['par1'] is not None:
                        job_data['par1'] = cleaned_data['par1']
                    if cleaned_data.has_key('par2') and cleaned_data['par2'] is not None:
                        job_data['par2'] = cleaned_data['par2']
                    if cleaned_data.has_key('par3') and cleaned_data['par3'] is not None:
                        job_data['par3'] = cleaned_data['par3']
                    if cleaned_data.has_key('calc_group') and cleaned_data['calc_group'] is not None:
                        job_data['calc_group'] = ocgisChoices(Config.CALCULATION_GROUP)[cleaned_data['calc_group']] 
                    if cleaned_data.has_key('calc_raw'):
                        job_data['calc_raw'] = bool(cleaned_data['calc_raw'])   
                    if cleaned_data.has_key('aggregate'):
                        job_data['aggregate'] = bool(cleaned_data['aggregate'])       
                    if cleaned_data.has_key('output_format'):
                        job_data['output_format'] = ocgisChoices(Config.OUTPUT_FORMAT)[cleaned_data['output_format']]   
                    if cleaned_data.has_key('prefix'):
                        job_data['prefix'] = cleaned_data['prefix']    
                    if cleaned_data.has_key('with_auxiliary_files'):
                        job_data['with_auxiliary_files'] = bool(cleaned_data['with_auxiliary_files'])                       
                            
            context.update({'job_data': job_data})
                    
        return context
    
    # method called after all forms have been processed and validated
    def done(self, form_list, **kwargs):
        
        # merge data from all forms
        form_data = {}
        for form in form_list:
            form_data.update( form.cleaned_data )
            
        # retrieve user from request context
        user = self.request.user
            
        # persist job specification to database
        job = OpenClimateGisJob.objects.create(status=JOB_STATUS.UNKNOWN,
                                               user=user,
                                               data_type=form_data['data_type'],
                                               long_name=form_data['long_name'],
                                               time_frequency=form_data['time_frequency'],
                                               dataset_category=form_data['dataset_category'],
                                               dataset=form_data['dataset'],
                                               dataset_category2=form_data['dataset_category2'],
                                               package_name=form_data['package_name'],
                                               geometry_category=str(form_data['geometry_category']),
                                               geometry_subcategory=str(form_data['geometry_subcategory']),
                                               # must transform list of integers into string
                                               geometry_id = ",".join(form_data['geometry_id']) if len(form_data['geometry_id'])>0 else None,
                                               latmin=form_data['latmin'],
                                               latmax=form_data['latmax'],
                                               lonmin=form_data['lonmin'],
                                               lonmax=form_data['lonmax'],
                                               lat=form_data['lat'],
                                               lon=form_data['lon'],
                                               agg_selection=form_data['agg_selection'],
                                               datetime_start=form_data['datetime_start'],
                                               datetime_stop=form_data['datetime_stop'],
                                               timeregion_month=",".join(form_data['timeregion_month']),
                                               timeregion_year=form_data['timeregion_year'],
                                               calc=form_data['calc'],
                                               par1=form_data['par1'],
                                               par2=form_data['par2'],
                                               par3=form_data['par3'],
                                               calc_raw=form_data['calc_raw'],
                                               calc_group=form_data['calc_group'],
                                               spatial_operation=form_data['spatial_operation'],
                                               aggregate=bool(form_data['aggregate']),
                                               output_format=form_data['output_format'],
                                               prefix=form_data['prefix'],
                                               with_auxiliary_files=form_data['with_auxiliary_files'] )
        
        # submit OCG job
        job.submit()
        
        # FIXME: pass OCG as additional argument to select jobs
        return HttpResponseRedirect(reverse('job_detail', args=[job.id, get_full_class_name(job)]))    
    
def get_geometries(request):
    '''Ajax method to return a JSON document containing geometry sub-types or geometry identifiers.'''
    
    response_data = {}
    category = request.GET.get('category', None)
    
    # 2nd request: category, subcategory --> geometries
    if 'subcategory' in request.GET:
        subcategory = request.GET.get('subcategory', None)
        response_data['geometries'] = ocgisGeometries.getGeometries(category, subcategory)
        
    # 1st request: type --> subtypes
    else:
        response_data['geometries'] = ocgisGeometries.getSubCategories(category)
    
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')


def get_datasets(request):
    '''Ajax method to return a JSON document containing the dataset selections, 
       for different possible query paramaters.'''
    
    data_type = request.GET.get('data_type', None)
    long_name = request.GET.get('long_name', None)
    time_frequency = request.GET.get('time_frequency', None)
    dataset_category = request.GET.get('dataset_category', None)
    dataset = request.GET.get('dataset', None)
    dataset_category2 = request.GET.get('dataset_category2', None)
    package_name = request.GET.get('package_name', None)
    
    #print 'GET Datasets request: %s' % request.GET
    json_data = {}
    # pass back the current selection
    json_data['request'] = { 'data_type':data_type, 'long_name':long_name, 'time_frequency':time_frequency, 
                             'dataset_category': dataset_category, 'dataset':dataset,
                             'dataset_category2': dataset_category2, 'package_name':package_name}
    datasets_dict = ocgisDatasets.getDatasetOptions(data_type, long_name=long_name, time_frequency=time_frequency, 
                                                    dataset_category=dataset_category, dataset=dataset,
                                                    dataset_category2=dataset_category2, package_name=package_name)
    # return all available options
    json_data['response'] = datasets_dict
        
    return HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

def get_metadata(request):
    '''Ajax method to return a JSON document containing the dataset metadata.''' 

    data_type = request.GET.get('data_type', None)
    long_name = request.GET.get('long_name', None)
    time_frequency = request.GET.get('time_frequency', None)
    dataset_category = request.GET.get('dataset_category', None)
    dataset = request.GET.get('dataset', None)
    dataset_category2 = request.GET.get('dataset_category2', None)
    package_name = request.GET.get('package_name', None)
    
    dict = ocgisDatasets.getDatasets(data_type, long_name=long_name, time_frequency=time_frequency, 
                                                dataset_category=dataset_category, dataset=dataset,
                                                package_name=package_name)
    
    # NOTE: must format datetime object as strings for JSON serialization
    dates = dict['metadata']['time_range']
    dict['metadata']['time_range'] = [ dates[0].strftime(DATETIME_FORMAT), dates[1].strftime(DATETIME_FORMAT) ]
    
    return HttpResponse(simplejson.dumps(dict['metadata']), mimetype='application/json')
    
    

    