#!/usr/bin/env python
import os, sys
import subprocess
import json
import gzip

from chert.config import config


annex_prefix = config.get('tmbnex', 'create_parent_path')

def addurl(url, filename):
    cmd = ['git-annex', 'addurl', '--file', filename, url]
    subprocess.check_call(cmd)

def get_posts_and_blogname(postsfile):
    print "POSTSFILE", postsfile
    if not postsfile.endswith('.json.gz'):
        raise RuntimeError, "bad file %s" % postsfile
    basename = os.path.basename(postsfile)
    blogname = basename.split('.json')[0]
    print "BLOGNAME", blogname, config
    posts = json.load(gzip.GzipFile(postsfile))
    return blogname, posts

def create_annex(annexdir):
    if not os.path.isdir(annexdir):
        cmd = ['git', 'init', annexdir]
        subprocess.check_call(cmd)

    oldpwd = os.getcwd()
    os.chdir(annexdir)

    if not os.path.isdir('.git/annex'):
        cmd = ['git-annex', 'init']
        subprocess.check_call(cmd)
    os.chdir(oldpwd)
    

args = sys.argv[1:]
if not len(args):
    raise RuntimeError, "need a file"

postsfile = args[0]
blogname, posts = get_posts_and_blogname(postsfile)


annexdir = os.path.join(annex_prefix, blogname)
create_annex(annexdir)


for filename, url in posts.items():
    if not os.path.isfile(filename):
        cmd = ['git-annex', 'addurl', '--file', filename, url]
        subprocess.call(cmd)
    else:
        print "File exists", filename


subprocess.check_call(['git-annex', 'sync'])

os.chdir(oldpwd)

    
