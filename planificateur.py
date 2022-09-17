import schedule
import time

def job1():
    print("I'm working...every minute")
def job2():
    print("I'm working...every hour")
def job3():
    print("I'm working...at 10:48")


schedule.every(1).minutes.do(job1)
schedule.every().hour.do(job2)
schedule.every().day.at("10:51").do(job3)

while 1:
    schedule.run_pending()
    time.sleep(1)