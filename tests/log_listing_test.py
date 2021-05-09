import os
import shlex, subprocess


def print_output(process):
    process.wait()
    stdout, stderr = process.communicate()
    if stdout:
        print("stdout:", stdout)

    if stderr:
        print("stderr:", stderr)


if __name__ == '__main__':
    symbol="BTC"
    quote="USDT"
    save_path = "../trades"
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    binance = subprocess.Popen(
        shlex.split(f"python ../luna_scripts/listing_log/binance_log.py {symbol+quote} {save_path} -d 3"),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    gate_io = subprocess.Popen(
        shlex.split(f"python ../luna_scripts/listing_log/gateio_log.py {symbol + '_' + quote} {save_path} -d 3"),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print_output(binance)
    print_output(gate_io)
