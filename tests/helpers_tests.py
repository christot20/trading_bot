import sys
import os
import platform
def mod_finder(): # module finder
    # must at least be in base directory of application to work
    path_to_dir = os.getcwd().split('trading_bot')[0] # path to trading_bot directory
    if platform.system() == 'Windows': # if on Windows
        new_dir = f"{path_to_dir}trading_bot\src" # src module
    else: # if on UNIX
        new_dir = f"{path_to_dir}trading_bot/src"
    return sys.path.insert(1, new_dir) # sets path for testing