import db
from datasets.maurer import *
from datasets.bcca_cccma_cgcm3 import *
from datasets.bcca_gfdl_cm2_1 import *
from datasets.hayhoe import *
from datasets.packages import *
import os
from datasets.base import itersubclasses, AbstractDataPackage, AbstractHarvestDataset


def get_subclasses(klass):
    ret = []
    for subclass in itersubclasses(klass):
        if not subclass.__name__.startswith('Abstract') and not subclass._exclude:
            ret.append(subclass)
    return(ret)

def main():
    models = get_subclasses(AbstractHarvestDataset)
    packages = get_subclasses(AbstractDataPackage)

    db_path = '/tmp/datasets.sqlite'
    if os.path.exists(db_path):
        os.remove(db_path)
    db.build_database(db_path=db_path)
    with db.session_scope(commit=True) as session:
        for model in models:
            m = model()
            print('inserting model: {0}'.format(m.__class__.__name__))
            m.insert(session)
            
        for package in packages:
            p = package()
            print('inserting package: {0}'.format(p.__class__.__name__))
            p.insert(session)


if __name__ == '__main__':
    main()
    print('success.')