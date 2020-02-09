import os
import subprocess
import sys

def check_if_is_loaded(dll_name, show_processes):
    proc = subprocess.Popen(['tasklist', "/m", dll_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = str(proc.communicate()[0], 'utf-8').strip()

    if show_processes:
        print(result)

    if "INFO: No tasks are running which match the specified criteria." == result:
        print("DLL NOT found")
    else:
        print("DLL found")


dll_name = sys.argv[1]
second_arg = ''
if len(sys.argv) > 2:
    second_arg = sys.argv[2]
show_option = True if second_arg == "show" else False

print("Checking if '{}' is loaded...".format(dll_name))
check_if_is_loaded(dll_name, show_option)