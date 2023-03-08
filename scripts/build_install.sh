#!/bin/bash
# Dinamically build and install latest pip version.

# Package variables
package_name="pubnub-python-metrics"
package_src="pubnub_python_metrics"
package_dist_src="pubnub_python_metrics"

# Get current directory parent dir
dir="$(pwd)"
parentdir="$(dirname "$dir")"

# Parse file containing version
file=${parentdir}/${package_name}/src/${package_src}/__about__.py
name=$(<"$file")       #the output of 'cat $file' is assigned to the $name variable
version=$(echo $name | cut -d \" -f2)  # might need to cut by \' instead of \"

# Build package
hatch build

# Install package
pip install -U dist/${package_dist_src}-${version}.tar.gz
