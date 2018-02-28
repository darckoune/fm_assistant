from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# On appelle la fonction setup

buildOptions = dict(
    packages = [],
    excludes = [],
    include_files=[os.path.join(PYTHON_INSTALL_DIR, 'DLLs') +'/tcl86t.dll', os.path.join(PYTHON_INSTALL_DIR, 'DLLs') + '/tk86t.dll']
)

setup(
    name = "salut",
    version = "0.1",
    description = "Ce programme vous dit bonjour",
    options = dict(build_exe = buildOptions),
    executables = [Executable("main.py")],
)
