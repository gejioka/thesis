# README #

### What is this repository for? ###

* Create backbone for multi-layer ad hoc networks
* https://github.com/gejioka/thesis

### Main features ###

* written in Python 2.7
* UNIX based platforms
* can create different kinds of backbones

### Installation ###
```sh
$ chmod +x install.sh
$ sudo ./install.sh
```

if get an error: ImportError: cannot import name sampling
```sh
$ sudo nano /usr/local/lib/python2.7/dist-packages/pymnet-0.1-py2.7.egg/pymnet/__init__.py
$ Comment out last line:
$ from . import sampling
$ Comment last line:
$ #from . import sampling
```

### Run Test ###
```sh
cd tools
python test_algorithms
```

### Run Program ###
```sh
python main.py -fp <filepath> -a <algorithm> --mcds --log -lv <logLevel> --plotting
```

### All parameters can use ###
| Argument | Description | Value |
| --- | --- | --- |
| -fp | Path of input file (network) | - |
| -p | Algorithm to calculate PCI value | x,cl |
| -a | Algorithm to create backbone | 1,2 |
| --cds | Create a Connected Dominating Set (CDS) for backbone | - |
| --mcds | Create a Minimum Connected Dominating Set (MCDS) for backbone | - |
| --rmcds | Create a Robust Minimum Connected Dominating Set (RMCDS) for backbone | - |
| --plotting | Tell program if needs to plot network | - |
| --clock | Track algorithm duration | - |
| --log | Add log messages | - |
| --level | Set log level of messages | - |
