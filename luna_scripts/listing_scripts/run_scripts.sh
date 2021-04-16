#!/bin/bash
if [ ! -d "../../trades" ]; then
	mkdir "../../trades"
fi
nohup python3 auto_mail.py > "../../outputs/mail_output.txt" &
nohup python3 auto_log.py > "../../outputs/log_output.txt" &

