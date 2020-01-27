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

with open(output, 'w') as f:
    yaml.dump({"test": {"requires": packages}}, f)

pyqt_patt = re.compile("pyqt=.")

commands = ["codecov"]
if any(pyqt_patt.match(pkg) for pkg in args.packages):
    commands.insert(0, "pytest --cov=psy_simple --cov-append -v tests/widgets")

with open(output, 'a') as f:
    yaml.dump({"test": {"commands": commands}}, f)
