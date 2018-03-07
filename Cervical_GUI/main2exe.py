"""
Allows to turn main.py into an executable file
"""
import os

TAB_SIZE = 13

USE_SAME_FILE = True

INPUT_FILE = "main.spec"
TMP_FILE = "main.spec.tmp"
OUTPUT_FILE = "new_main.spec"
PYINSTALLER_OPTIONS = ['--onefile', '--icon="icone.ico"', '--noconsole']

HIDDEN_IMPORTS = ['scipy.special._ufuncs_cxx',
                'scipy.linalg.cython_blas',
                'scipy.linalg.cython_lapack',
                'scipy.integrate',
                'scipy.integrate.quadrature',
                'scipy.integrate.odepack',
                'scipy.integrate._odepack',
                'scipy.integrate.quadpack',
                'scipy.integrate._quadpack',
                'scipy.integrate._ode',
                'scipy.integrate.vode',
                'scipy.integrate._dop',
                'scipy.integrate.lsoda',
                'scipy.interpolate',
                'scipy.linalg',
                'scipy.linalg.misc',
                'scipy.linalg.blas',
                'scipy._lib.messagestream',
                'sklearn.neighbors.typedefs',
                'pywt._extensions._cwt']

PATH_TO_PROJECT = 'C:\\Users\\Guillaume\\Documents\\GitHub\\projetlong\\Cervical_GUI'
PATH_TO_PYTHON_INSTALL = 'C:\\Users\\Guillaume\\AppData\\Local\\Programs\\Python\\' \
                         'Python36-32\\Lib\\site-packages\\scipy\\extra-dll'


PATHEX = [PATH_TO_PROJECT, PATH_TO_PYTHON_INSTALL]


pyinstaller_command = "pyinstaller " + " ".join(PYINSTALLER_OPTIONS) + " main.py"
print("Running " + pyinstaller_command)
os.system(pyinstaller_command)
print("pyinstaller done")

print("Changing variables")

with open(INPUT_FILE, 'r') as input_file, open(TMP_FILE, 'w') as output_file:
    for line in input_file.readlines():
        if "hiddenimports" in line:
            print("Changing hiddenimports")
            output_file.write(TAB_SIZE * ' ')
            output_file.write("hiddenimports=[\n")
            for hidden_import in HIDDEN_IMPORTS:
                output_file.write(2*TAB_SIZE*' ')
                output_file.write("'{0}',\n".format(hidden_import))

            output_file.write(TAB_SIZE * ' ')
            output_file.write("],\n")
            print("Changed hiddenimports")
        elif "pathex" in line:
            print("Changing pathex")
            output_file.write(TAB_SIZE * ' ')
            output_file.write("pathex=[\n")
            for path_ex in PATHEX:
                output_file.write(2*TAB_SIZE*' ')
                output_file.write("'{0}',\n".format(path_ex.replace('\\', '\\\\')))

            output_file.write(TAB_SIZE * ' ')
            output_file.write("],\n")
            print("Changed pathex")
        else:
            output_file.write(line)

print("Changed variables")
print("Moving file")

if USE_SAME_FILE:
    os.remove(INPUT_FILE)
    os.rename(TMP_FILE, INPUT_FILE)
else:
    os.rename(TMP_FILE, OUTPUT_FILE)

print("Generating exe")
os.system("pyinstaller main.spec")
print("Generated exe")
print("Moving exe")
os.remove('main.exe')
os.rename('dist\\main.exe', 'Cervical Kine Recorder.exe')

print("Done")