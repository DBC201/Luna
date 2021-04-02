import dateparser
import time
import calendar


if __name__ == '__main__':
    raw_time = "2021-28-3 11:46:31 UTC"
    parsed_time = dateparser.parse(raw_time)
    epoch_time = calendar.timegm(parsed_time.timetuple())
    while True:
        current_time = time.time()
        print(current_time, epoch_time)
        if current_time >= epoch_time:
            print(time.localtime())
            break
        time.sleep(1)
