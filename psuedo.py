# -*- coding: utf-8 -*-
print("Psuedo-Intelligence | Release | Version 1.0 [BETA RELEASE]")
print("Warning: Psuedo-Intelligence is still in beta development and is not ready for release to the general public yet. If you find any errors, remember that this app is in beta, and please open an issue on GitHub.")
from MiscCode import MCode, loading_window, rscpath
import threading
mc = MCode()
lw = loading_window()
t00 = threading.Thread(target=lw.create_window)
t00.start()
t000 = threading.Thread(target=mc.play_intro)
t000.start()
import whisper # stt module
import pyaudio # records audio
import wave # saves audio to file
from pydub import AudioSegment # converts to mp3
import pvporcupine # wake word
from pvrecorder import PvRecorder # wake word
from keystrokes import *
from win11toast import toast as notify
import webbrowser as wb
import os
from openai import OpenAI
import time
import string
import asyncio
import ctypes
from tkinter import *
from tkinter.ttk import *
import test_INITIATEBSOD as bsod
import keyboard
import win32clipboard
from sympy.solvers import solve
from sympy import Symbol
from test_HTMLTK import responseNotification
print("Module initialization: SUCCESS")

if os.path.exists("apikey.txt"):
	pass
else:
	print("warning: No OpenAI Apikey found.")
	key = input("Input Apikey: ")
	with open("apikey.txt", "a") as f:
		f.write(key)

with open("apikey.txt", "r") as f:
	apikey = f.read()
	
lw.update_image("loading_2.png")
client = OpenAI(api_key=apikey)
gpttrain = [{"role": "system", "content": "You are a helpful assistant."}]
systrain2 = """Hello, ChatGPT! You are now MessageSorterAI. When you recieve a query, sort it into one of the following categories:
 [1] New File
 [2] Open File
 [3] Google Search
 [4] Open Browser
 [5] Open Command Prompt
 [6] Open Canvas
 [7] Exit
 [8] Lock Machine
 [9] Close All Applications
 [10] Initiate BSOD
 [11] Calculate Selected Text
Please follow these rules:
If the query has arguments:
<Number>~<arguments>
(e.g. the user said 'search up where is pasadena'):
you would return:
3~where is pasadena
If the query does not have arguments:
<Number>
(e.g. the user said 'Can you open a file?')
you would return:
2
If the user's query doesn't match any of these, but ChatGPT could answer it (e.x. the user said 'where is pasadena'), output:
0
If the user's query doesn't match any of these, but it might be possible with Python code (e.x. the user said 'open Psiphon 3'), output:
-1
"""
gpttrain2 = [
	{
		"role": "system",
		"content": systrain2
	},
	{
		"role": "user",
		"content": "search up youtube official website"
	},
	{
		"role": "assistant",
		"content": "3~youtube offical website"
	},
	{
		"role": "user",
		"content": "can you lock my screen"
	},
	{
		"role": "assistant",
		"content": "8"
	},
	{
		"role": "user",
		"content": "who won the 2014 world series in baseball"
	},
	{
		"role": "assistant",
		"content": "0"
	},
	{
		"role": "user",
		"content": "turn up my volume"
	},
	{
		"role": "assistant",
		"content": "-1"
	}
]
print("OpenAI initialization: SUCCESS")

lw.update_image("loading_3.png")
porcupine = pvporcupine.create(access_key="yp3b8tbirddwwURxXHkfHO7EqQnDUfXnjpHjOIG1C2yyUEI+906Uug==", keywords=["computer"])
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
print("Porcupine initialization: SUCCESS")

lw.update_image("loading_4.png")

def skip_operation(argument):
	global KeepExecuting
	KeepExecuting = False
def remove_punctuation(text):
	return text.translate(str.maketrans('', '', string.punctuation))
print("Function initialization: SUCCESS")
lw.update_image(rscpath("loading_5.png"))
def showNtfn(title, msg, duration):
	try:
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(
			notify(title=title, body=msg, app_id="Psuedo-Intelligence", duration=str(duration))
		)
	except Exception as e: # An error *will* occur. Save some output.
		pass#print(f"Error in showNtfn: {e}\nIgnoring as error is not fatal.")
def aiNtfy():
	try:
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(
			notify(title="Command Not Found", body="PS-I didn't recognize that. PS-I will attempt to process your command using A.I.\nClick to skip AI request", app_id="Psuedo-Intelligence", duration=str(5), on_click=skip_operation)
		)
	except Exception as e: # An error *will* occur. Save some output.
		pass #print(f"Error in aiNtfy: {e}\nIgnoring as error is not fatal.")

print("Notification initialization: SUCCESS")
lw.update_image("loading_6.png")
model = whisper.load_model("tiny") # load model 02
print("Loading whisper model: SUCCESS")
lw.update_image("loading_7.png")
time.sleep(1)
t00 = threading.Thread(target=lw.destroy_window)
t00.start()

t1 = threading.Thread(target=showNtfn, args=("Ready", "Psuedo Intelligence is now listening for \"Computer\"!", 5,))
t1.start()

recorder.start()
while True:
	keyword_index = porcupine.process(recorder.read())
	if keyword_index >= 0:
		t2 = threading.Thread(target=showNtfn, args=("Listening...", "You can start talking now.", 2,))
		t2.start()

		# Record and transcribe audio
		mc.record_audio(wav_filename='output.wav', mp3_filename='output.mp3')  # record audio
		print("Done. Transcribing audio.")
		resultfull = model.transcribe("output.mp3", fp16="false")  # transcribe audio
		resultwpunc = resultfull["text"]
		result = remove_punctuation(resultfull["text"].lower())
		print("Done. User said:", resultwpunc) # print the result
		print("(This will be processed) User said (without punctuation):", result)
		print("Processing...")

		gpttrain2.append({"role": "user", "content": result})
		response0 = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=gpttrain2
		)
		response_0 = response0.choices[0].message.content
		print(response_0)
		response_0 = response_0.split("~")
		task2run = response_0[0]
		try:
			arguments = response_0[1]
		except:
			arguments = ""
		if task2run == "1":
			t3 = threading.Thread(target=showNtfn, args=("Creating New File", "Sending keystrokes.", 3,))
			t3.start()
			PressKey(VK_CONTROL)
			PressKey(VK_N)
			ReleaseKey(VK_CONTROL)
			ReleaseKey(VK_N)
		elif task2run == "2":
			t4 = threading.Thread(target=showNtfn, args=("Opening File", "Sending keystrokes.", 3,))
			t4.start()
			PressKey(VK_CONTROL)
			PressKey(VK_O)
			ReleaseKey(VK_CONTROL)
			ReleaseKey(VK_O)
		elif task2run == "3":
			t5 = threading.Thread(target=showNtfn, args=("Searching", f"Google Searching \"{arguments}\"", 3,))
			t5.start()
			googlesearch = f"https://www.google.com/search?q={arguments.replace(' ', '+')}"
			wb.open(googlesearch)
		elif task2run == "4":
			t6 = threading.Thread(target=showNtfn, args=("Opening Browser", "Opening Browser to google.com...", 3,))
			t6.start()
			wb.open_new_tab("https://www.google.com/")
		elif task2run == "5":
			t7 = threading.Thread(target=showNtfn, args=("Opening Command Prompt", "Starting cmd.exe...", 3,))
			t7.start()
			os.system("start cmd.exe")
		elif task2run == "6":
			t10 = threading.Thread(target=showNtfn, args=("Opening Canvas", "Opening Canvas...", 3,))
			t10.start()
			wb.open_new_tab("https://pearland.instructure.com")
		elif task2run == "7":
			exit()
		elif task2run == "8":
			t11 = threading.Thread(target=showNtfn, args=("Locking Machine", "Locking workstation in 5 seconds...", 3,))
			t11.start()
			time.sleep(5)
			ctypes.windll.user32.LockWorkStation()
		elif task2run == "9":
			t12 = threading.Thread(target=showNtfn, args=("Closing All Apps", "Closing all apps in 3 seconds...", 3,))
			t12.start()
			time.sleep(3)
			mc.closeApps()
		elif task2run == "10":
			t13 = threading.Thread(target=showNtfn, args=("What's blue?", "The sky! Oh, and this.", 3,))
			t13.start()
			time.sleep(3)
			bsod._goodbye()
		elif task2run == "11":
			# Copy the selected text
			PressKey(VK_CONTROL)
			PressKey(VK_C)
			ReleaseKey(VK_CONTROL)
			ReleaseKey(VK_C)
			# Get copied text and therefore selection
			win32clipboard.OpenClipboard()
			e = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

		elif task2run == "0":
			global KeepExecuting
			KeepExecuting = True
			t8 = threading.Thread(target=aiNtfy)
			t8.start()
			time.sleep(5)
			if KeepExecuting:
				pass
			else:
				continue
			gpttrain.append({"role": "user", "content": resultwpunc})
			response = client.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=gpttrain
			)
			aisponse = responseNotification(response.choices[0].message.content)
		elif task2run == "-1":
			print("Initiate TripleA call.")
			t14 = threading.Thread(target=showNtfn, args=("Sorry!", "TripleA capabilites aren't supported yet. Check back in version 1.1.", 3,))
			t14.start()
		else:
			print(task2run)
			print("Capability Not Supported")
		print("completed!")