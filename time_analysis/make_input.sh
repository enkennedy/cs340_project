#!/bin/bash

perl ../make_random_input.pl 5000 $1 20 20 constraints_$1classes.txt prefs_$1classes.txt

perl ../make_random_input.pl 5000 1000 20 $1 constraints_$1students.txt prefs_$1students.txt