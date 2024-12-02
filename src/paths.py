import os

# root directory of project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# module directories
CONFIG_DIR = os.path.join(BASE_DIR, "config")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
