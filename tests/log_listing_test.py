import os
import shlex, subprocess


if __name__ == '__main__':
    symbol = "ethusdt"
    save_path = "../trades"
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    process = subprocess.Popen(
        shlex.split(f"python ../luna_scripts/listing_log/log_listing.py {symbol} {save_path} -d 3"),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    stdout, stderr = process.communicate()
    if stdout:
        print("stdout:", stdout.decode())

    if stderr:
        print("stderr:", stderr.decode())
