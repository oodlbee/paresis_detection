import time

class StartTimer(object):
    def __init__(self):
        self.time_seek_delta = 0
        self.is_paused = True
        self.start_time = time.perf_counter()

    def pause(self):
        self.pause_begin_time = time.perf_counter()
        self.is_paused = True

    def resume(self):
        delay = time.perf_counter() - self.pause_begin_time
        self.start_time += delay
        self.is_paused = False

    def update_start_time(self):
        """Update only in pause"""
        if self.is_paused:
            self.resume()
            self.pause()
        else:
            raise Exception("Can update time only in pause")

    def seek(self, time_seek):
        """Seeks only in pause"""
        if self.is_paused:
            self.update_start_time()
        current_time = time.perf_counter() - self.start_time
        self.time_seek_delta = time_seek - current_time


    def get_current_time(self):
        return time.perf_counter() + self.time_seek_delta - self.start_time
    
    def frame_delay(self, frame_time):
        return frame_time - self.get_current_time()


