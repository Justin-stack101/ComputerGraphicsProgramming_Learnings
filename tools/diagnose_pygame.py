import sys
import os
from pathlib import Path
print('cwd=', os.getcwd())
print('executable=', sys.executable)
print('version=', sys.version)
print('sys.path=', sys.path)
try:
    import pygame
    print('pygame import OK', pygame.__version__)
except Exception as e:
    print('pygame import failed', type(e).__name__, e)
try:
    import pkgutil
    print('setuptools._distutils spec=', pkgutil.find_spec('setuptools._distutils'))
except Exception as e:
    print('pkgutil check failed', type(e).__name__, e)
for p in ['python', 'py', sys.executable]:
    print('which', p)
    try:
        import subprocess
        out = subprocess.run([p, '--version'], capture_output=True, text=True, check=False)
        print(out.stdout.strip())
        print(out.stderr.strip())
    except Exception as e:
        print('which failed', p, type(e).__name__, e)
print('done')
