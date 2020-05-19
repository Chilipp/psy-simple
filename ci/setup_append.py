# Script to generate conda build config to be appended
import argparse
import os.path as osp
import yaml
import re

parser = argparse.ArgumentParser()

parser.add_argument('recipe_dir', help="Path to the conda recipe directory")
parser.add_argument(
    "packages", nargs="+", metavar="PACKAGE=VERSION",
    help="Package specifications to include in the test.requires section")

args = parser.parse_args()

output = osp.join(args.recipe_dir, 'recipe_append.yaml')
packages = []

for pkg in args.packages:
    if pkg.strip().endswith("="):  # no version specified
        packages.append(pkg.strip()[:-1])
    else:
        packages.append(pkg)

config = {"test": {
    "requires": packages,
    "commands": ["codecov",
                 """python -c 'import shutil; shutil.rmtree("tests")'"""]
    }}

pyqt_patt = re.compile("pyqt=.")
if any(pyqt_patt.match(pkg) for pkg in args.packages):

    config["test"]["commands"].insert(
        0, "pytest --cov=psy_simple --cov-append -v tests/widgets")
    config["test"]["imports"] = ["psy_simple.widgets"]
    config["test"]["requires"].append("psyplot-gui")
    # HACK: Should be removed when https://github.com/ipython/ipykernel/pull/489
    # is implemented
    config["test"]["requires"].append("jupyter_client <6.0.0")

with open(output, 'w') as f:
    yaml.dump(config, f)
