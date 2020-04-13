from os.path import abspath, dirname
from glob import glob
from setuptools import setup, Extension
from distutils.sysconfig import get_config_vars

ROOT_PATH = abspath(dirname(__file__))

with open('version.txt') as f:
    VERSION = f.read().strip()

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

with open('CHANGES.md') as f:
    CHANGES = f.read()

extension_options = {
    'sources': glob('src/**/*.cpp', recursive=True),
    'include_dirs': ['include'],
    'define_macros': [('JCORMS_VERSION', VERSION)],
    'depends': glob('include/**/*.h*', recursive=True),
}

cfgvars = get_config_vars()
cxx = cfgvars.get('CXX')
if cxx and 'g++' in cxx:
    # Avoid warning about invalid flag for C++
    for varname in ('CFLAGS', 'OPT'):
        value = cfgvars.get(varname)
        if value and '-Wstrict-prototypes' in value:
            cfgvars[varname] = value.replace('-Wstrict-prototypes', '')

    # Add -pedantic, so we get a warning when using non-standard features, and
    # -Wno-long-long to pacify old gcc (or Apple's hybrids) that treat "long
    # long" as an error under C++ (see issue #69)
    extension_options['extra_compile_args'] = ['-pedantic', '-Wno-long-long']

setup(
    name='jcorms',
    version=VERSION,
    description='JSON-C Object Relational Mapping Structures',
    long_description=LONG_DESCRIPTION + '\n\n' + CHANGES,
    long_description_content_type='text/markdown',
    license='MIT License',
    keywords='json ctypes ffi',
    author='Randy Eckman',
    author_email='emanspeaks@gmail.com',
    url='https://github.com/emanspeaks/jcorms',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
    ],
    ext_modules=[Extension('jcorms', **extension_options)],
    python_requires='>=3.7'
)
