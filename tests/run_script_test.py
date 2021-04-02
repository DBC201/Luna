import shlex, subprocess

if __name__ == '__main__':
    process = subprocess.Popen(
        shlex.split("python ./datetime_test.py"), # python3 for linux
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    stdout, stderr = process.communicate()
    print(stdout.decode())
