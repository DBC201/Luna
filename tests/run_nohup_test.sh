#!/bin/bash
if ! [ -d "../trades" ]; then
	mkdir "../trades"
else
	echo "trades folder exist"
fi
nohup python3 "../luna_scripts/listing_scripts/log_listing.py" btcusdt "sfad" > "../outputs/test.txt" &
#intentionally wrong command for testing
