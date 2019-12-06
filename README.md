Illumina Unpace
-------------------------------------------------
Tools like Basespace have made accessing sequence files easier, however if multiple copies of the same sequence are generated the nested file structure can become frustrating to deal with. This tool aims to index the nested file structure, detect fastq.gz files within, determine if there are duplicates and choose the larger file, and place all sequences in an output directory. 

## Prerequisities
* Linux
* Python 3 (installed and in path)
* pip3 v.19.2.1

## Install

```shell
$ git clone git@github.com:lorentzben/Illumina_Unpack.git
```
TODO fill out what else will be in here
After cloning a folder called Illumina_Unpack will be created. Inside will be this README and unpack_illumina.py

## Help
```shell
$ python3 unpack_illumina.py -h 

```


## Running 
```shell
$ chmod +x unpack_illumina.py
$ python3 unpack_illumina.py -n NAME
```
Ensure that the name of the nested folder from basespace The results of analysis will be placed ____ 

TODO fill in where this location is


## Output
TODO fill in names

Inside of the directory ______there will be _______

## Current Files
* unpack_illumina.py
* README.md

## Version
* Version 1.0

## Author
* Ben Lorentz

## Future Plans
* Find file structure
* Log all files found and filesizes
* Check log for duplicates
* Move files into output dir
* Implement verbose logging at the info and debugging scale
* Implememt unit testing using the unittest package
* Move final files into a output directory 
