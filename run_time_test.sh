#!/bin/bash

echo "$1 classes..."
sh run.sh time_analysis/constraints_$1classes.txt time_analysis/prefs_$1classes.txt time_analysis/schedule_$1classes.txt
perl is_valid.pl time_analysis/constraints_$1classes.txt time_analysis/prefs_$1classes.txt time_analysis/schedule_$1classes.txt

echo "$1 students..."
sh run.sh time_analysis/constraints_$1students.txt time_analysis/prefs_$1students.txt time_analysis/schedule_$1students.txt
perl is_valid.pl time_analysis/constraints_$1students.txt time_analysis/prefs_$1students.txt time_analysis/schedule_$1students.txt