from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], "include_files": ['assets/']}

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, target_name='LazyHub',
               icon="assets\\cat.ico")
]

setup(name='LazyHub',
      version='3.0.5',
      description='Warframe ahk scripts',
      options={'build_exe': build_options},
      executables=executables)
