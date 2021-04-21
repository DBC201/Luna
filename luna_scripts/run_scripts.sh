#!/bin/bash
output_path="$(pwd)/../../outputs"
if [ ! -d output_path ]; then
	mkdir $output_path
fi

nohup python3 auto_mail.py > "$output_path/mail_output.txt" &
nohup python3 auto_log.py > "$output_path/log_output.txt" &
