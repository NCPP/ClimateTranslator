import ncpp
import os

def getAbsolutePath(relativePath):
    '''Returns the absolute path for a path relative to the top-level 'ncpp' module.'''
    
    return os.path.join(os.path.split(os.path.abspath(ncpp.__file__))[0], relativePath)