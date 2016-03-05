#!/usr/bin/env bash

iterations=1000


python3 recon.py -c 2 -l 2 -n 1 >> results.2016-03.dat

time for probability in 0.1 0.01 0.001; do
	for constraints in 2 4 8 16 32 ; do
		for langs in 2 4 8 16 32 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat
		done;
	done;
done;

date; echo "done: { 2 4 8 16 32 } ^ 2"

time for probability in 0.1 0.01 0.001; do
	for constraints in 64 ; do
		for langs in 2 4 8 16 32 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat
		done;
	done;
done;

date; echo "done: 64 * { 2 4 8 16 32 }"

for probability in 0.1 0.01 0.001; do
	for constraints in 128 ; do
		for langs in 2 4 8 16 32 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat
		done;
	done;
done;

date; echo "done: 128 * { 2 4 8 16 32 }"

for probability in 0.1 0.01 0.001; do
	for constraints in 2 4 8 16 32 ; do
		for langs in 64 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat
		done;
	done;
done;

date; echo "done: { 2 4 8 16 32 } * 64"

for probability in 0.1 0.01 0.001; do
	for constraints in 2 4 8 16 32 ; do
		for langs in 128 ; do
			echo $probability $constraints $langs;
			python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $langs >> results.2016-03.dat
		done;
	done;
done;

date; echo "done: { 2 4 8 16 32 } * 128"

constraints=64
languages=64
for probability in 0.1 0.01 0.001; do
	echo $probability $constraints $langs;
	python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $languages >> results.2016-03.dat
done;
date; echo "done: $constraints * $languages"

constraints=64
languages=128
for probability in 0.1 0.01 0.001; do
	echo $probability $constraints $langs;
	python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $languages >> results.2016-03.dat
done;
date; echo "done: $constraints * $languages"

constraints=128
languages=64
for probability in 0.1 0.01 0.001; do
	echo $probability $constraints $langs;
	python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $languages >> results.2016-03.dat
done;
date; echo "done: $constraints * $languages"

constraints=128
languages=128
for probability in 0.1 0.01 0.001; do
	echo $probability $constraints $langs;
	python3 recon.py -noheader -n $iterations -p $probability -c $constraints -l $languages >> results.2016-03.dat
done;
date; echo "done: $constraints * $languages"


