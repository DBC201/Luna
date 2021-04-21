#!/bin/bash

mail_pid=$(ps aux | grep python3 | awk '{if ($12 == "auto_mail.py"){print $2}}')
sudo kill -9 $mail_pid
log_pid=$(ps aux | grep python3 | awk '{if ($12 == "auto_log.py"){print $2}}')
sudo kill -9 $log_pid
