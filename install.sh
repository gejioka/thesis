#!/bin/bash

# Update system
echo "Update..."
apt update;

# Install pip and networkx
echo "Install pip..."
apt install -y python-pip;

# Install networkx
echo "Install networkx..."
pip install networkx;

#Install matplotlib
echo "Install matplotlib..."
apt-get install -y python-matplotlib;

# Install git
echo "Install git..."
apt-get install -y git;

# Install mercurial
echo "Install mercurial..."
apt install -y mercurial;

# Install numpy
echo "Install numpy..."
apt install -y python-numpy;

# Install scipy
echo "Install scipy..."
apt-get install -y python-scipy;

apt-get install python-setuptools;

# Download multi-layer networks library
echo "Clone multi-layer networks library..."
#hg clone https://bitbucket.org/bolozna/multilayer-networks-library

echo "Install multi-layer networks library..."
#mv multilayer-networks-library/* .
python setup.py install;

# Disable sampling
echo "Disable sampling..."
sed -i 's/from . import sampling/#from . import sampling/g' /usr/local/lib/python2.7/dist-packages/pymnet-0.1-py2.7.egg/pymnet/__init__.py;

# Remove folders
echo "Remove folders..."
rm -r multilayer-networks-library;
rm -r pymnet.egg-info;
rm -r build;
rm -r dist;
rm -r doc;

# Remove files
echo "Remove files..."
rm bitbucket-pipelines.yml;
rm LICENSE.txt;
rm MANIFEST.in;
rm tox.ini;
rm README.md;
rm setup.py;
