from pathlib import Path
import subprocess
out = Path('debug_pip_versions.txt')
lines = []
cmds = [
    ['python', '-m', 'pip', '--version'],
    ['python', '-m', 'pip', 'index', 'versions', 'pygame'],
    ['python', '-m', 'pip', 'index', 'versions', 'pygame-ce'],
    ['python', '-m', 'pip', 'install', 'pygame', '--dry-run'],
    ['python', '-m', 'pip', 'install', 'pygame-ce', '--dry-run']
]
for cmd in cmds:
    lines.append('CMD: ' + ' '.join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=120)
        lines.append('RC: ' + str(r.returncode))
        lines.append('STDOUT:')
        lines.append(r.stdout)
        lines.append('STDERR:')
        lines.append(r.stderr)
    except Exception as e:
        lines.append('EXC: ' + repr(e))
    lines.append('-' * 40)
out.write_text('\n'.join(lines))
print('wrote', out.resolve())
