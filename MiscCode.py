import pyaudio
import wave
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from pydub import AudioSegment
import threading
import os
import sys

apdpth = os.getenv('APPDATA')

class MCode():
	def play_intro(self):
		chunk = 1024
		f = wave.open(rscpath("intro.wav"), "rb")
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
						channels = f.getnchannels(),
						rate = f.getframerate(),
						output = True)
		data = f.readframes(chunk)
		while data:
			stream.write(data)
			data = f.readframes(chunk)
		stream.stop_stream()
		stream.close()
		p.terminate()

	def get_wav_duration(self, file_path):
		with wave.open(rscpath(file_path), 'rb') as wav_file:
			frames = wav_file.getnframes()
			rate = wav_file.getframerate()
			duration = frames / float(rate)
		return duration

	def record_audio(self, wav_filename, mp3_filename, channels=1, rate=44100, chunk=1024, silence_threshold=2):
		p = pyaudio.PyAudio()
	
		# Ensure correct types for p.open() parameters
		format = pyaudio.paInt16  # 16-bit resolution, should be an integer
		channels = int(channels)  # Number of channels should be an integer
		rate = int(rate)  # Sampling rate should be an integer
		chunk = int(chunk)  # Buffer size should be an integer

		stream = p.open(format=format, 
						channels=channels, 
						rate=rate, 
						input=True, 
						frames_per_buffer=chunk)
	
		print("Recording...")
		frames = []
		silent_chunks = 0
		silence_limit = int(rate / chunk * silence_threshold)

		while True:
			data = stream.read(chunk)
			frames.append(data)

			# Convert audio data to numpy array for volume calculation
			audio_data = np.frombuffer(data, np.int16).astype(np.float32)

			# Calculate the volume as the root mean square (RMS) of the audio data
			volume = np.sqrt(np.mean(audio_data**2))

			# If the volume is below a certain threshold, count it as silence
			if volume < 500:  # Adjust this threshold as necessary
				silent_chunks += 1
			else:
				silent_chunks = 0

			if silent_chunks > silence_limit:
				break

		print("Recording finished.")
		stream.stop_stream()
		stream.close()
		p.terminate()

		# Save the recording to a WAV file
		wf = wave.open(rscpath(wav_filename), 'wb')
		wf.setnchannels(channels)
		wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
		wf.setframerate(rate)
		wf.writeframes(b''.join(frames))
		wf.close()

		print(f"Saved as {wav_filename}")

		audio = AudioSegment.from_wav(rscpath(wav_filename))
		audio.export(rscpath(mp3_filename), format="mp3")
		print(f"Saved as {mp3_filename}")

	def get_process_id_from_hwnd(self, hwnd):
		"""Get the process ID from a window handle."""
		tid, pid = win32process.GetWindowThreadProcessId(hwnd)
		return pid

	def closeApps(self):
		current_pid = os.getpid()
		exclusions = ["cmd.exe", "explorer.exe", "python.exe", "devenv.exe"]

		window_handles = gw.getAllWindows()

		for window in window_handles:
			if window.title:
				try:
					hwnd = window._hWnd
					pid = get_process_id_from_hwnd(hwnd)
					process_name = psutil.Process(pid).name()

					if pid != current_pid and process_name not in exclusions:
						psutil.Process(pid).terminate()
						try:
							window.close()
						except gw.PyGetWindowException as e:
							print(f"Warning: Could not close '{window.title}' - {str(e)}")
				except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, IndexError):
					pass

class loading_window():
	def create_window(self):
		self.root = Tk()
		self.root.overrideredirect(True)
		self.root.attributes('-topmost', True)
		self.root.wm_attributes('-transparentcolor', '#dd181f')
		self.root.config(bg='#dd181f')
		image = Image.open(rscpath("loading_1.png"))
		self.photo = ImageTk.PhotoImage(image)
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		img_width, img_height = image.size
		x = (screen_width // 2) - (img_width // 2)
		y = (screen_height // 2) - (img_height // 2)
		self.root.geometry(f'{img_width}x{img_height}+{x}+{y}')
		self.label1 = Label(self.root, image=self.photo, bg='#dd181f', bd=0)
		self.label1.pack()
		self.root.attributes('-alpha', 1.0)
		
		self.root.mainloop()

	def update_image(self, new_image_path):
		new_image_path = rscpath(new_image_path)
		self.root.after(0, self._update_image, new_image_path)

	def _update_image(self, new_image_path):
		new_image = Image.open(new_image_path)
		new_photo = ImageTk.PhotoImage(new_image)
		self.label1.config(image=new_photo)
		self.label1.image = new_photo

	def destroy_window(self):
		self.root.after(0, self.root.destroy)

def rscpath(relative_path):
	try:
		base_path = sys._MEIPASS
		return os.path.join(base_path, relative_path)
	except AttributeError:
		return relative_path # When EXE aint compiled, return the path untouched
