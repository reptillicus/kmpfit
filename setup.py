from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
from glob import glob
import sys, os

try:
   import numpy
except:
   print '''
-- Error.
kmpfit requires NumPy, which seems to be unavailable here.
Please check your Python installation.
'''
   sys.exit(1)


include_dirs = ["."]
numdir = os.path.dirname(numpy.__file__)
ipath = os.path.join(numdir, numpy.get_include())
include_dirs.append(ipath)
include_dirs.append('src')

short_descr = "kmpfit"

description = """

    * A function to search for gaussian components in a profile (module
      profiles) and a class for non-linear least squares curve fitting
      (module kmpfit)
   """


define_macros = []

# MS Windows adjustments
#
if sys.platform == 'win32':
    define_macros.append(('YY_NO_UNISTD_H', None))
    define_macros.append(('_CRT_SECURE_NO_WARNINGS', None))

# avoid using buggy Apple compiler
#
if sys.platform=='darwin':
   from distutils import ccompiler
   import subprocess
   import re
   c = ccompiler.new_compiler()
   process = subprocess.Popen(c.compiler+['--version'], stdout=subprocess.PIPE)
   output = process.communicate()[0].strip()
   version = output.split()[0]
   if re.match('i686-apple-darwin[0-9]*-llvm-gcc-4.2', version):
      os.environ['CC'] = 'clang'

setup(
   name="kmpfit",
   version="1.0",
   description=short_descr,
   long_description=description,
   platforms = ['Linux', 'Mac OSX', 'Windows'],
   license = 'BSD',
   ext_package='kmpfit',
   packages = ['kmpfit'], 
   ext_modules=[
      Extension("kmpfit", sources=["src/kmpfit.c", "src/mpfit.c"], include_dirs=include_dirs)
   ],
)
