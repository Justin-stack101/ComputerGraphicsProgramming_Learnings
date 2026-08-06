import shutil
import subprocess
from pathlib import Path
out = Path('winget_debug_output.txt')
lines = []
lines.append(f'cwd={Path.cwd()}')
winget_path = shutil.which('winget')
lines.append(f'winget_path={winget_path}')
if winget_path:
    try:
        r = subprocess.run([winget_path, 'search', 'python'], capture_output=True, text=True, timeout=120)
        lines.append('returncode=' + str(r.returncode))
        lines.append('stdout=')
        lines.append(r.stdout)
        lines.append('stderr=')
        lines.append(r.stderr)
    except Exception as e:
        lines.append('search_error=' + repr(e))
else:
    lines.append('winget_not_found')
try:
    import sys
    lines.append('python_exe=' + sys.executable)
    lines.append('python_version=' + sys.version)
except Exception as e:
    lines.append('python_info_error=' + repr(e))
out.write_text('\n'.join(lines))
print('wrote', out.resolve())
