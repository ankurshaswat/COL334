#!/bin/bash

fileName=`date +"%d/%T"`
nmap -sn 10.208.26.0/24>"logResults/"$fileName
