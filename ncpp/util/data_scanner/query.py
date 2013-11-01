import db
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.orm.exc import NoResultFound


class DataQuery(object):
    
    def __init__(self,db_path=None):
        if db_path is not None:
            db.connect(db_path)
        self.db_path = db_path
        
    def get_package(self,*args,**kwds):
        '''
        :param dataset_category: The name of the dataset category.
        :type dataset_category: str
        :param package_name: The name of the package.
        :type dataset_category: str
        :raises: NoResultFound
        :returns: A dictionary with keys corresponding to options. The key values are lists of options.
        :rtype: dict
        '''
        
        with db.session_scope() as session:
            
            kwds['session'] = session
            query = self._get_package_query_(*args,**kwds)

            if query.count() >= 1:
                ret = {'dataset_category':[obj.dataset_category.name for obj in query],
                       'package_name':[obj.name for obj in query]}
                for v in ret.itervalues(): v.sort()
            else:
                raise(NoResultFound)
                
        return(ret)
    
    def get_package_datasets(self,*args,**kwds):
        '''
        Same parameters as `get_package`. This method must return a
        single row.
        
        :raises: NoResultFound, MultipleResultsFound
        :rtype: list containing a 1 or more dictionaries
        :returns: A dictionary with two keys: 'dataset' and 'metadata'. The 'dataset'
        key contains a list of dictionaries suitable to pass as a single argument
        to `ocgis.RequestDatasetCollection`. The 'metadata' key contains description
        and other fields such as 'time_range'.
        '''
        
        with db.session_scope() as session:
            
            kwds['session'] = session
            query = self._get_package_query_(*args,**kwds)
            package = query.one()
            dataset = [f.get_request_dataset_kwargs() for f in package.field]
            ret = {'dataset':dataset,
                   'metadata':{'description':{'package':package.description,
                                              'dataset_category':package.dataset_category.description},
                               'time_range':[package.time_start,package.time_stop]}}
            return(ret)
    
    def _get_package_query_(self,dataset_category=None,package_name=None,time_range=None,session=None):
            
        query = session.query(db.DataPackage).join(db.DatasetCategory)
        
        if dataset_category is not None:
            query = query.filter(db.DatasetCategory.name == dataset_category)
        if package_name is not None:
            query = query.filter(db.DataPackage.name == package_name)
        if time_range is not None:
            start,stop = time_range
            and_start = and_(db.DataPackage.time_start <= start,db.DataPackage.time_stop >= start)
            and_stop = and_(db.DataPackage.time_start <= stop,db.DataPackage.time_stop >= stop)
            query = query.filter(or_(and_start,and_stop))
                
        return(query)
        
    def get_variable_or_index(self,*args,**kwds):
        '''
        :param select_data_by: One of "variable" or "index".
        :type select_data_by: str
        :param long_name: A variable's or index's long name representation.
        :type long_name: str
        :param dataset_category: The name of the dataset category.
        :type dataset_category: str
        :param dataset: The name of the containing dataset.
        :type dataset: str
        :param time_frequency: One of "day", "month", or "year".
        :type time_frequency: str
        :param time_range: List with two elements corresponding to lower and upper time selection boundaries.
        :type time_rage: [datetime.datetime,datetime.datetime]
        :raises: NoResultFound
        :returns: A dictionary with keys corresponding to options. The key values are lists of options.
        :rtype: dict
        '''
        
        with db.session_scope() as session:
            
            kwds['session'] = session
            query = self._get_variable_or_index_query_(*args,**kwds)
            
            if query.count() >= 1:
                to_collect = ['long_name','time_frequency','dataset_category','dataset']
                ret = {tc:[] for tc in to_collect}
                for obj in query.all():
                    for tc in to_collect:
                        ret[tc].append(getattr(obj,tc))
                for k,v in ret.iteritems():
                    new = list(set(v))
                    new.sort()
                    ret[k] = new
            else:
                raise(NoResultFound)
    
        return(ret)
    
    def get_variable_or_index_dataset(self,*args,**kwds):
        '''
        Same parameters as `get_variable_or_index`. This method must return a
        single row.
        
        :raises: NoResultFound, MultipleResultsFound
        :rtype: list containing a single dictionary
        :returns: A dictionary with two keys: 'dataset' and 'metadata'. The 'dataset'
        key contains a list of dictionaries suitable to pass as a single argument
        to `ocgis.RequestDatasetCollection`. The 'metadata' key contains description
        and other fields such as 'time_range'.
        '''
        
        with db.session_scope() as session:
            
            kwds['session'] = session
            query = self._get_variable_or_index_query_(*args,**kwds)
            field = session.query(db.Field).filter(db.Field.fid == query.one().fid).one()
            dataset = field.get_request_dataset_kwargs()
            ret = {'dataset':[dataset],
                   'metadata':{'description':{'long_name':field.clean_variable.description,
                                              'dataset':field.container.dataset.description,
                                              'dataset_category':field.container.dataset.dataset_category.description},
                               'time_range':[field.container.time_start,field.container.time_stop]}}
            return(ret)
    
    def _get_variable_or_index_query_(self,select_data_by,long_name=None,time_frequency=None,
                                      dataset_category=None,dataset=None,time_range=None,
                                      session=None):
        
        cquery = session.query(db.Container.cid,
                                   db.Container.time_start,
                                   db.Container.time_stop,
                                   db.Container.time_frequency,
                                   db.Dataset.name.label('dataset'),
                                   db.DatasetCategory.name.label('dataset_category'))
        cquery = cquery.join(db.Container.dataset,db.Dataset.dataset_category).subquery()
        
        cs = [db.CleanVariable.long_name,db.Field.fid] + [c for c in cquery.c]
        query = session.query(*cs).filter(db.Field.type == select_data_by)
        query = query.join(db.Field.clean_variable)
        query = query.filter(cquery.c.cid == db.Field.cid)

        if long_name is not None:
            query = query.filter(db.CleanVariable.long_name == long_name)
        
        if time_frequency is not None:
            query = query.filter(cquery.c.time_frequency == time_frequency)

        if dataset_category is not None:
            query = query.filter(cquery.c.dataset_category == dataset_category)
        
        if dataset is not None:
            query = query.filter(cquery.c.dataset == dataset)
            
        if time_range is not None:
            start,stop = time_range
            and_start = and_(cquery.c.time_start <= start,cquery.c.time_stop >= start)
            and_stop = and_(cquery.c.time_start <= stop,cquery.c.time_stop >= stop)
            query = query.filter(or_(and_start,and_stop))
        
        return(query)
