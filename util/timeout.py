import time
import signal

# 处理超时的函数
def test(i):
    time.sleep(i%4)
    print("within time")
    return i


def handler(signum, frame):
    raise Exception("timeout")

if __name__ == "__main__":

    i = 0
    for i in range(10):
        try:
            signal.signal(signal.SIGALRM, handler)
            # 设置定时
            signal.alarm(3)
            test(i)
            i += 1
            signal.alarm(0)
        except Exception as e:
            print(e)
        finally:
            print(i)