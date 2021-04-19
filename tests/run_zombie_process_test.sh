#!/bin/bash
if [ ! -d "../outputs" ]; then
	mkdir "../outputs"
fi

python3 zombie_process_test.py > "../outputs/zombie_test_output.txt" &
