import PyInstaller.__main__
import os
import argparse
import sys
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nuitka', help="Use Nuitka instead of PyInstaller", action='store_true')

args = parser.parse_args()

if not args.nuitka:
    PyInstaller.__main__.run([
        '--name=%s' % 'EzTwitchPlays',
        '--specpath=%s' % os.path.join('.', 'exe'),
        '--distpath=%s' % os.path.join('.', 'exe'),
        '--icon=%s' % os.path.join('.', 'EzTP.ico'),
        '--onedir',
        '--clean',
        '--noconsole',
        '--noconfirm',
        os.path.join('.', 'main.py')
    ])

else:
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--output-filename=%s' % 'EzTwitchPlays',
        '--mode=%s' % 'standalone',
        '--follow-imports',
        'main.py'
    ]
    # subprocess.run(cmd, capture_output=False, text=True)
    raise NotImplementedError("Haven't figured out Nuitka yet...")