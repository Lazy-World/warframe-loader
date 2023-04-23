from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], "include_files": ['assets/']}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, target_name='LazyHub',
               icon="assets\\cat.ico")
]

setup(name='LazyHub',
      version='3.0.7',
      description='LazyHub',
      options={'build_exe': build_options},
      executables=executables)
