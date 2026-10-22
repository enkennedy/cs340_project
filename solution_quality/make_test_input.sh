#!/bin/bash

perl ../make_random_input.pl $1 $2 $3 $4 test$5/constraints_$5a.txt test$5/prefs_$5a.txt

perl ../make_random_input.pl $1 $2 $3 $4 test$5/constraints_$5b.txt test$5/prefs_$5b.txt

perl ../make_random_input.pl $1 $2 $3 $4 test$5/constraints_$5c.txt test$5/prefs_$5c.txt

perl ../make_random_input.pl $1 $2 $3 $4 test$5/constraints_$5d.txt test$5/prefs_$5d.txt

perl ../make_random_input.pl $1 $2 $3 $4 test$5/constraints_$5e.txt test$5/prefs_$5e.txt