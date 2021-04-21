#!/bin/bash
current_path=$(realpath "$0")
output_path="$current_path/../../outputs"
if [ ! -d output_path ]; then
	mkdir $output_path
fi

cd "$current_path/listing_mail"
nohup python3 auto_mail.py > "$output_path/mail_output.txt" &
cd ..

cd "$current_path/listing_log"
nohup python3 auto_log.py > "$output_path/log_output.txt" &
cd ..
