#!/bin/bash

fileName=`date +"%d/%T"`
nmap -sn 10.184.29.0/24>"logResults/"$fileName
