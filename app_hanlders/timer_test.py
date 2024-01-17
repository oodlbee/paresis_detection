from video_timer import StartTimer
import time

timer = StartTimer()
start_time = time.perf_counter()
time.sleep(1)

assert(round(time.perf_counter() - start_time, 3) == round(timer.get_current_time(), 3))

timer.pause()
time.sleep(1)
timer.update_start_time()

assert(int(timer.get_current_time()) == 1)

timer.seek(5)

assert(int(timer.get_current_time()) == 5)

timer.seek(10)

assert(int(timer.get_current_time()) == 10)

timer.seek(3)

assert(int(timer.get_current_time()) == 3)



timer.resume()
time.sleep(1)
timer.pause()

assert(int(timer.get_current_time()) == 4)

