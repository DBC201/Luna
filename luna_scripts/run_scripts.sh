#!/bin/bash
current_path=$(dirname "$(realpath "$0")")
output_path="$current_path/../outputs"
if [ ! -d "$output_path" ]; then
	mkdir "$output_path"
fi

cd "$current_path/listing_mail"
nohup python3 auto_mail.py > "$output_path/mail_output.txt" &
cd ..

cd "$current_path/listing_log"
python download_gateio.py > ../../outputs/download_gateio.txt &
# nohup python3 auto_log.py > "$output_path/log_output.txt" &
cd ..

# cd "$current_path/meme"
# nohup python3 DiscordBot.py > "$output_path/meme_output.txt" &
# cd ..

# echo "Active python3 processes:"
# ps aux | grep python3
