import av
import gc
import logging
import threading
import tkinter as tk
import numpy as np
import sounddevice as sd
from typing import Tuple, Dict
from application.app_handlers.video_timer import StartTimer
from PIL import ImageTk, Image, ImageOps
logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used


class TkinterVideo(tk.Label):
    def __init__(self, master, scaled: bool = True, keep_aspect: bool = False, *args, **kwargs):
        super(TkinterVideo, self).__init__(master, *args, **kwargs)
        self._video_thread = None
        self._resume_video_event = threading.Event()

        self._paused = True
        self._container = None

        self._current_img = None
        self._frame_number = 0
        self._audio_frame_number = 0
        self._time_stamp = 0

        self.av_time_base = av.time_base
        self._current_frame_size = (0, 0)

        self._video_info = {
            "duration": 0, # duration of the video
            "framerate": 0, # frame rate of the video
            "time_base": 0,
            "framesize": (0, 0), # tuple containing frame height and width of the video
            "audio_sample_rate": 0,
            "frames_num": 0

        }   

        self.set_scaled(scaled)
        self._keep_aspect_ratio = keep_aspect
        self._resampling_method: int = Image.NEAREST
        self.bind("<<Destroy>>", self._cleanup)
    

    def keep_aspect(self, keep_aspect: bool):
        """ keeps the aspect ratio when resizing the image """
        self._keep_aspect_ratio = keep_aspect


    def set_resampling_method(self, method: int):
        """ sets the resampling method when resizing """
        self._resampling_method = method


    def set_size(self, size: Tuple[int, int], keep_aspect: bool=False):
        """ sets the size of the video """
        self.set_scaled(False, self._keep_aspect_ratio)
        self._current_frame_size = size
        self._keep_aspect_ratio = keep_aspect


    def _resize_event(self, event):
        self._current_frame_size = event.width, event.height

        if self._paused and self._current_img and self.scaled:
            if self._keep_aspect_ratio:
                proxy_img = ImageOps.contain(self._current_img.copy(), self._current_frame_size)

            else:
                proxy_img = self._current_img.copy().resize(self._current_frame_size)
            
            self._current_imgtk = ImageTk.PhotoImage(proxy_img)
            self.config(image=self._current_imgtk)


    def set_scaled(self, scaled: bool, keep_aspect: bool = False):
        self.scaled = scaled
        self._keep_aspect_ratio = keep_aspect
        if scaled:
            self.bind("<Configure>", self._resize_event)
        else:
            self.unbind("<Configure>")
            self._current_frame_size = self.video_info()["framesize"]


    def _set_frame_size(self):
        """ sets frame size to avoid unexpected resizing """
        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._video_info["framesize"], (255, 0, 0, 0)))
        self.config(width=self._video_info["framesize"][0], height=self._video_info["framesize"][1], image=self.current_imgtk)
        self._current_frame_size = self._video_info["framesize"][0], self._video_info["framesize"][1]

    def _frame_preview(self):
        """previews one frame"""
        frame = next(self._container.decode(video=0))
        self._time_stamp = float(frame.pts * self._video_info["time_base"])
        width, height = self._current_frame_size[0] ,self._current_frame_size[1]
        if self._keep_aspect_ratio:
            im_ratio = frame.width / frame.height
            dest_ratio = width / height
            if im_ratio != dest_ratio:
                if im_ratio > dest_ratio:
                    new_height = round(frame.height / frame.width * width)
                    height = new_height
                else:
                    new_width = round(frame.width / frame.height * height)
                    width = new_width
        self._current_img = frame.to_image(width=width, height=height, interpolation="FAST_BILINEAR")

        if self.current_imgtk.width() == self._current_img.width and self.current_imgtk.height() == self._current_img.height:
            self.current_imgtk.paste(self._current_img)
        else:
            self.current_imgtk = ImageTk.PhotoImage(self._current_img)
        self.config(image=self.current_imgtk)


    def _resume_audio(self):
        """resumes the audio"""
        self._audio_frame_number = int(self._time_stamp * self._video_info['audio_sample_rate'])
        if self._audio_frame_number < len(self.audio):
            sd.play(self.audio[self._audio_frame_number:])


    def _play_video(self):
        """ load's file from a thread """
        current_thread = threading.current_thread()
        
        while self._video_thread == current_thread:
            if self._paused:
                self._resume_video_event.wait()
                self._resume_video_event.clear()
                continue
    
            try:
                frame = next(self._container.decode(video=0))
                self._time_stamp = float(frame.pts * self._video_info["time_base"])
                width, height = self._current_frame_size[0] ,self._current_frame_size[1]

                if self._keep_aspect_ratio:
                    im_ratio = frame.width / frame.height
                    dest_ratio = width / height
                    if im_ratio != dest_ratio:
                        if im_ratio > dest_ratio:
                            new_height = round(frame.height / frame.width * width)
                            height = new_height
                        else:
                            new_width = round(frame.width / frame.height * height)
                            width = new_width
                self._current_img = frame.to_image(width=width, height=height, interpolation="FAST_BILINEAR")

                if self.current_imgtk.width() == self._current_img.width and self.current_imgtk.height() == self._current_img.height:
                    self.current_imgtk.paste(self._current_img)
                else:
                    self.current_imgtk = ImageTk.PhotoImage(self._current_img)
                delay = self.timer.frame_delay(self._time_stamp)
                self.after(int(max(delay, 0)*1000), self.config(image=self.current_imgtk))
                self._frame_number += 1
                self.event_generate("<<FrameGenerated>>")

                if self._frame_number % 5 == 0:
                    self.event_generate("<<UpdateScale>>")

            except (StopIteration, av.error.EOFError):
                try:
                    self.event_generate("<<Ended>>")
                except tk.TclError:
                    self._cleanup()
                self._container.seek(0)
                self._frame_number = 0
                self._time_stamp = 0
                self.timer = StartTimer()
                self.timer.pause()
                self.pause()
                continue
            except tk.TclError:
                self._cleanup()

        if self._container:
            self._cleanup()
            

    def _cleanup(self):
        """cleans up after closing"""
        if self._container:
            self._container.close()
        sd.stop()
        self._frame_number = 0
        self._paused = True
        self._container.close()
        if self._video_thread:
            self._video_thread = None
        if self._container:
            self._container.close()
            self._container = None
        gc.collect()
        self._container = None


    def load(self, path: str):
        """ loads the file from the given path """
        self._container = av.open(path)
        self._container.discard_corrupt = True
        self._container.streams.video[0].thread_type = "AUTO"
        self._container.streams.audio[0].thread_type = "AUTO"

        stream_video = self._container.streams.video[0]
        stream_audio = self._container.streams.audio[0]

        try:
            self._video_info["framerate"] = stream_video.average_rate
            self._video_info["frames_num"] = stream_video.frames
            self._video_info["time_base"] = stream_video.time_base
            self._video_info["duration"] = float(stream_video.duration * self._video_info["time_base"])
            self._video_info['audio_sample_rate'] = stream_audio.rate
            self._video_info["framesize"] = (stream_video.width, stream_video.height)   
        except (TypeError, tk.TclError):
            raise TypeError("Not a video file")
        
        self.audio = []
        for frame in self._container.decode(stream_audio):
            self.audio.append(frame.to_ndarray()[0])
        self.audio = np.array(self.audio).flatten()
        sd.default.samplerate = self._video_info['audio_sample_rate']

        self._container.seek(0)
        
        self._set_frame_size()
        self._frame_preview()
        self._paused = True
        self.timer = StartTimer()
        self.timer.pause()
        self._video_thread = threading.Thread(target=self._play_video, daemon=True)
        self._video_thread.start()
        self.event_generate("<<Loaded>>")


    def pause(self):
        """ pauses the video file """
        self._paused = True
        sd.stop()
        self.timer.pause()


    def play(self):
        """ plays the video file """
        self._paused = False
        self._resume_video_event.set()
        self._resume_audio()
        self.timer.resume()


    def seek(self, frame: int):
        """ seeks to specific time""" 
        self._frame_number = frame
        seek_value = int(frame/self._video_info["framerate"]*self.av_time_base)
        self._container.seek(seek_value, whence='time', backward=True, any_frame=False) # the seek time is given in av.time_base, the multiplication is to correct the frame
        self._frame_preview()
        self.timer.seek(self._time_stamp)
        self._resume_video_event.set()


    def is_paused(self):
        """ returns if the video is paused """
        return self._paused


    def video_info(self) -> Dict:
        """ returns dict containing duration, frame_rate, file"""
        return self._video_info


    def metadata(self) -> Dict:
        """ returns metadata if available """
        if self._container:
            return self._container.metadata
        return {}


    def current_frame_number(self) -> int:
        """ return current frame number """
        return self._frame_number


    def current_duration(self) -> float:
        """ returns current playing duration in sec """
        return self._time_stamp
    

    def current_img(self) -> Image:
        """ returns current frame image """
        return self._current_img        