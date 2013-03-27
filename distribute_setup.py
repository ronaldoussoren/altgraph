"""
Distribute/setuptools bootstrap helper.

This is a fork of the official distribute bootstrap script with two
changes:

    1) Only supports 'use_setuptools()', without arguments, and does
       not support proper installation.

    2) Automaticly uses the most recent version of distribute/setuptools
"""

SETUPTOOLS_PACKAGE='distribute'

import os
import sys
import time
import fnmatch
import tempfile
import tarfile
import urllib
from distutils import log
try:
    from hashlib import md5

except ImportError:
    from md5 import md5

try:
    import subprocess

    def _python_cmd(*args):
        args = (sys.executable,) + args
        return subprocess.call(args) == 0

except ImportError:
    def _python_cmd(*args):
        args = (sys.executable,) + args
        new_args = []
        for a in args:
            new_args.append(a.replace("'", "'\"'\"'"))
        os.system(' '.join(new_args)) == 0


try:
    import json

    def get_pypi_src_download(package):
        url = 'https://pypi.python.org/pypi/%s/json'%(package,)
        fp = urllib.urlopen(url)
        try:
            try:
                data = fp.read()

            finally:
                fp.close()
        except urllib.error:
            raise RuntimeError("Cannot determine download link for %s"%(package,))

        pkgdata = json.loads(data)
        if 'urls' not in pkgdata:
            raise RuntimeError("Cannot determine download link for %s"%(package,))

        for info in pkgdata['urls']:
            if info['packagetype'] == 'sdist' and info['url'].endswith('tar.gz'):
                return (info.get('md5_digest'), info['url'])

except ImportError:
    # Python 2.5 compatibility, no JSON in stdlib but luckily JSON syntax is
    # simular enough to Python's syntax to be able to abuse the Python compiler

    import _ast as ast

    def get_pypi_src_download(package):
        url = 'https://pypi.python.org/pypi/%s/json'%(package,)
        fp = urllib.urlopen(url)
        try:
            try:
                data = fp.read()

            finally:
                fp.close()
        except urllib.error:
            raise RuntimeError("Cannot determine download link for %s"%(package,))


        a = compile(data, '-', 'eval', ast.PyCF_ONLY_AST)
        if not isinstance(a, ast.Expression):
            raise RuntimeError("Cannot determine download link for %s"%(package,))

        a = a.body
        if not isinstance(a, ast.Dict):
            raise RuntimeError("Cannot determine download link for %s"%(package,))

        for k, v in zip(a.keys, a.values):
            if not isinstance(k, ast.Str):
                raise RuntimeError("Cannot determine download link for %s"%(package,))

            k = k.s
            if k == 'urls':
                a = v
                break
        else:
            raise RuntimeError("PyPI JSON for %s doesn't contain URLs section"%(package,))

        if not isinstance(a, ast.List):
            raise RuntimeError("Cannot determine download link for %s"%(package,))

        for info in v.elts:
            if not isinstance(info, ast.Dict):
                raise RuntimeError("Cannot determine download link for %s"%(package,))
            url = None
            packagetype = None
            chksum = None

            for k, v in zip(info.keys, info.values):
                if not isinstance(k, ast.Str):
                    raise RuntimeError("Cannot determine download link for %s"%(package,))

                if k.s == 'url':
                    if not isinstance(v, ast.Str):
                        raise RuntimeError("Cannot determine download link for %s"%(package,))
                    url = v.s

                elif k.s == 'packagetype':
                    if not isinstance(v, ast.Str):
                        raise RuntimeError("Cannot determine download link for %s"%(package,))
                    packagetype = v.s

                elif k.s == 'md5_digest':
                    if not isinstance(v, ast.Str):
                        raise RuntimeError("Cannot determine download link for %s"%(package,))
                    chksum = v.s

            if url is not None and packagetype == 'sdist' and url.endswith('.tar.gz'):
                return (chksum, url)

        raise RuntimeError("Cannot determine download link for %s"%(package,))

def _build_egg(egg, tarball, to_dir):
    # extracting the tarball
    tmpdir = tempfile.mkdtemp()
    log.warn('Extracting in %s', tmpdir)
    old_wd = os.getcwd()
    try:
        os.chdir(tmpdir)
        tar = tarfile.open(tarball)
        _extractall(tar)
        tar.close()

        # going in the directory
        subdir = os.path.join(tmpdir, os.listdir(tmpdir)[0])
        os.chdir(subdir)
        log.warn('Now working in %s', subdir)

        # building an egg
        log.warn('Building a Distribute egg in %s', to_dir)
        _python_cmd('setup.py', '-q', 'bdist_egg', '--dist-dir', to_dir)

    finally:
        os.chdir(old_wd)
    # returning the result
    log.warn(egg)
    if not os.path.exists(egg):
        raise IOError('Could not build the egg.')


def _do_download(to_dir, packagename=SETUPTOOLS_PACKAGE):
    tarball = download_setuptools(packagename, to_dir)
    version = tarball.split('-')[-1][:-7]
    print version
    egg = os.path.join(to_dir, 'distribute-%s-py%d.%d.egg'
                       % (version, sys.version_info[0], sys.version_info[1]))
    if not os.path.exists(egg):
        _build_egg(egg, tarball, to_dir)
    sys.path.insert(0, egg)
    import setuptools
    setuptools.bootstrap_install_from = egg


def use_setuptools():
    # making sure we use the absolute path
    return _do_download(os.path.abspath(os.curdir))

def download_setuptools(packagename, to_dir):
    # making sure we use the absolute path
    to_dir = os.path.abspath(to_dir)
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    chksum, url = get_pypi_src_download(packagename)
    tgz_name = os.path.basename(url)
    saveto = os.path.join(to_dir, tgz_name)

    src = dst = None
    if not os.path.exists(saveto):  # Avoid repeated downloads
        try:
            log.warn("Downloading %s", url)
            src = urlopen(url)
            # Read/write all in one block, so we don't create a corrupt file
            # if the download is interrupted.
            data = src.read()

            if chksum is not None:
                data_sum = md5(data).hexdigest()
                if data_sum != chksum:
                    raise RuntimeError("Downloading %s failed: corrupt checksum"%(url,))


            dst = open(saveto, "wb")
            dst.write(data)
        finally:
            if src:
                src.close()
            if dst:
                dst.close()
    return os.path.realpath(saveto)



def _extractall(self, path=".", members=None):
    """Extract all members from the archive to the current working
       directory and set owner, modification time and permissions on
       directories afterwards. `path' specifies a different directory
       to extract to. `members' is optional and must be a subset of the
       list returned by getmembers().
    """
    import copy
    import operator
    from tarfile import ExtractError
    directories = []

    if members is None:
        members = self

    for tarinfo in members:
        if tarinfo.isdir():
            # Extract directories with a safe mode.
            directories.append(tarinfo)
            tarinfo = copy.copy(tarinfo)
            tarinfo.mode = 448 # decimal for oct 0700
        self.extract(tarinfo, path)

    # Reverse sort directories.
    if sys.version_info < (2, 4):
        def sorter(dir1, dir2):
            return cmp(dir1.name, dir2.name)
        directories.sort(sorter)
        directories.reverse()
    else:
        directories.sort(key=operator.attrgetter('name'), reverse=True)

    # Set correct owner, mtime and filemode on directories.
    for tarinfo in directories:
        dirpath = os.path.join(path, tarinfo.name)
        try:
            self.chown(tarinfo, dirpath)
            self.utime(tarinfo, dirpath)
            self.chmod(tarinfo, dirpath)
        except ExtractError:
            e = sys.exc_info()[1]
            if self.errorlevel > 1:
                raise
            else:
                self._dbg(1, "tarfile: %s" % e)
