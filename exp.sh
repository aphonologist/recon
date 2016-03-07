#!/usr/bin/env bash

iterations=1000

python3 recon.py -n 1 >> results.2016-03.dat

for probability in 0.1 0.01 0.001 ; do
	for constraints in 2 4 8 16 32 64 128 ; do
		for langs in 2 4 8 16 32 64 128 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat &
		done;
	done;
done;
