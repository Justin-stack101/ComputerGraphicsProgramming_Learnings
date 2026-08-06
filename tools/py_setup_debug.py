from pathlib import Path
import subprocess
import shutil
import sys
out = Path(r'C:\Users\justi\Downloads\School Files\MainProjectCollection\Computer Graphics Programming\py_setup_debug.txt')
lines = []
lines.append(f'cwd={Path.cwd()}')
lines.append(f'exe={sys.executable}')
lines.append(f'version={sys.version}')
for cmd in ['python', 'py', 'winget']:
    spec = shutil.which(cmd)
    lines.append(f'which_{cmd}={spec}')
    try:
        r = subprocess.run([cmd, '--version'], capture_output=True, text=True, check=False)
        lines.append(f'{cmd}_rc={r.returncode}')
        lines.append(f'{cmd}_out={r.stdout.strip()}')
        lines.append(f'{cmd}_err={r.stderr.strip()}')
    except Exception as e:
        lines.append(f'{cmd}_error={e!r}')
commands = [
    ['python', '-m', 'pip', '--version'],
    ['python', '-m', 'pip', 'index', 'versions', 'pygame'],
    ['python', '-m', 'pip', 'index', 'versions', 'pygame-ce'],
    ['python', '-m', 'pip', 'install', '--only-binary', ':all:', 'pygame-ce'],
    ['python', '-m', 'pip', 'install', '--only-binary', ':all:', 'pygame'],
    ['python', '-m', 'pip', 'install', 'pygame'],
]
for cmd in commands:
    lines.append('CMD=' + ' '.join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=300)
        lines.append('rc=' + str(r.returncode))
        lines.append('stdout=' + r.stdout.strip())
        lines.append('stderr=' + r.stderr.strip())
    except Exception as e:
        lines.append('cmd_error=' + repr(e))
    lines.append('-'*80)
try:
    import pygame
    lines.append('pygame_import_ok=' + pygame.__version__)
except Exception as e:
    lines.append('pygame_import_fail=' + repr(e))
out.write_text('\n'.join(lines))
print('wrote', out)
