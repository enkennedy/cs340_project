#!/bin/bash

echo "------------------------------------------------------" 
echo "running test $1a..."
sh run.sh solution_quality/test$1/constraints_$1a.txt solution_quality/test$1/prefs_$1a.txt solution_quality/test$1/schedule_$1a.txt
perl is_valid.pl solution_quality/test$1/constraints_$1a.txt solution_quality/test$1/prefs_$1a.txt solution_quality/test$1/schedule_$1a.txt

echo "------------------------------------------------------" 
echo "running test $1b..."
sh run.sh solution_quality/test$1/constraints_$1b.txt solution_quality/test$1/prefs_$1b.txt solution_quality/test$1/schedule_$1b.txt
perl is_valid.pl solution_quality/test$1/constraints_$1b.txt solution_quality/test$1/prefs_$1b.txt solution_quality/test$1/schedule_$1b.txt

echo "------------------------------------------------------" 
echo "running test $1c..."
sh run.sh solution_quality/test$1/constraints_$1c.txt solution_quality/test$1/prefs_$1c.txt solution_quality/test$1/schedule_$1c.txt
perl is_valid.pl solution_quality/test$1/constraints_$1c.txt solution_quality/test$1/prefs_$1c.txt solution_quality/test$1/schedule_$1c.txt

echo "------------------------------------------------------" 
echo "running test $1d..."
sh run.sh solution_quality/test$1/constraints_$1d.txt solution_quality/test$1/prefs_$1d.txt solution_quality/test$1/schedule_$1d.txt
perl is_valid.pl solution_quality/test$1/constraints_$1d.txt solution_quality/test$1/prefs_$1d.txt solution_quality/test$1/schedule_$1d.txt

echo "------------------------------------------------------" 
echo "running test $1e"
sh run.sh solution_quality/test$1/constraints_$1e.txt solution_quality/test$1/prefs_$1e.txt solution_quality/test$1/schedule_$1e.txt
perl is_valid.pl solution_quality/test$1/constraints_$1e.txt solution_quality/test$1/prefs_$1e.txt solution_quality/test$1/schedule_$1e.txt