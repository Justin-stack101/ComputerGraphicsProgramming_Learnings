import subprocess
from pathlib import Path
out = Path('install_pygame_ce_log.txt')
lines = []
commands = [
    ['python', '-m', 'pip', '--version'],
    ['python', '-m', 'pip', 'index', 'versions', 'pygame-ce'],
    ['python', '-m', 'pip', 'install', '--only-binary', ':all:', 'pygame-ce'],
    ['python', '-c', 'import pygame; print(pygame.__version__)']
]
for cmd in commands:
    lines.append('CMD: ' + ' '.join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=False)
        lines.append('returncode=' + str(r.returncode))
        lines.append('stdout:')
        lines.append(r.stdout.strip())
        lines.append('stderr:')
        lines.append(r.stderr.strip())
    except Exception as e:
        lines.append('EXC: ' + repr(e))
    lines.append('-' * 40)
out.write_text('\n'.join(lines))
print('log written to', out.resolve())
