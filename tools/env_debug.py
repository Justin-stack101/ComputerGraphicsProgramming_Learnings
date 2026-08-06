import sys
import os
from pathlib import Path
import shutil
import subprocess
out_path = Path('env_debug.txt')
lines = []
lines.append(f'cwd={Path.cwd()}')
lines.append(f'python_executable={sys.executable}')
lines.append(f'python_version={sys.version}')
lines.append(f'python_path={sys.path}')
lines.append(f'PATH={os.environ.get("PATH","")[:2000]}')
for cmd in ['python', 'py', 'winget']:
    try:
        which = shutil.which(cmd)
        lines.append(f'which_{cmd}={which}')
    except Exception as e:
        lines.append(f'which_{cmd}_error={e!r}')
    try:
        r = subprocess.run([cmd, '--version'], capture_output=True, text=True, check=False)
        lines.append(f'{cmd}_version_rc={r.returncode}')
        lines.append(f'{cmd}_version_stdout={r.stdout.strip()}')
        lines.append(f'{cmd}_version_stderr={r.stderr.strip()}')
    except Exception as e:
        lines.append(f'{cmd}_version_error={e!r}')
for cmd in [sys.executable, 'py', 'winget']:
    try:
        r = subprocess.run([cmd, '-0p'] if cmd != sys.executable else [cmd, '-V'], capture_output=True, text=True, check=False)
        lines.append(f'{cmd}_list_rc={r.returncode}')
        lines.append(f'{cmd}_list_stdout={r.stdout.strip()}')
        lines.append(f'{cmd}_list_stderr={r.stderr.strip()}')
    except Exception as e:
        lines.append(f'{cmd}_list_error={e!r}')
for cmd in [[sys.executable, '-m', 'pip', '--version'], [sys.executable, '-m', 'pip', 'index', 'versions', 'pygame'], [sys.executable, '-m', 'pip', 'install', '--only-binary', ':all:', 'pygame']]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=False)
        lines.append(f'cmd={cmd}')
        lines.append(f'returncode={r.returncode}')
        lines.append(f'stdout={r.stdout.strip()}')
        lines.append(f'stderr={r.stderr.strip()}')
    except Exception as e:
        lines.append(f'cmd_error={cmd} {e!r}')
out_path.write_text('\n'.join(lines))
print('wrote', out_path.resolve())
