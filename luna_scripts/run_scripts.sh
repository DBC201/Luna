#!/bin/bash
current_path=$(pwd)
output_path="output_path/../../outputs"
if [ ! -d output_path ]; then
	mkdir $output_path
fi

nohup python3 auto_mail.py > "$output_path/mail_output.txt" &
nohup python3 auto_log.py > "$output_path/log_output.txt" &
