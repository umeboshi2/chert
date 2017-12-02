import os
import hashlib
import subprocess
import json

from unipath.path import Path as path
from unipath import FILES, DIRS, LINKS
from git import Repo


#http://code.activestate.com/recipes/576620-changedirectory-context-manager/
class WorkingDirectory(object):
    def __init__(self, directory):
        self._dir = directory
        self._cwd = os.getcwd()
        self._pwd = self._cwd

    @property
    def current(self):
        return self._cwd

    @property
    def previous(self):
        return self._pwd

    @property
    def relative(self):
        c = self._cwd.split(os.path.sep)
        p = self._pwd.split(os.path.sep)
        l = min(len(c), len(p))
        i = 0
        while i < l and c[i] == p[i]:
            i += 1
        return os.path.normpath(os.path.join(*(['.'] + (['..'] * (len(c) - i)) + p[i:])))

    def __enter__(self):
        self._pwd = self._cwd
        os.chdir(self._dir)
        self._cwd = os.getcwd()
        return self

    def __exit__(self, *args):
        os.chdir(self._pwd)
        self._cwd = self._pwd
        

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_sha256sum(fileobj):
    s = hashlib.new('sha256')
    block = fileobj.read(4096)
    while block:
        s.update(block)
        block = fileobj.read(4096)
    return s.hexdigest()

def get_sha256sum_string(string):
    s = hashlib.new('sha256')
    s.update(string)
    return s.hexdigest()

def trailing_slash(dirname):
    if not dirname.endswith('/'):
        return '%s/' % dirname
    return dirname

def remove_trailing_slash(pathname):
    while pathname.endswith('/'):
        pathname = pathname[:-1]
    return pathname

    

def parse_config_lines(filename):
    return [line.strip() for line in file(filename)
            if line.strip() and not line.strip().startswith('#')]

