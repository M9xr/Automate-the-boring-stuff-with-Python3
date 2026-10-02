# YouTube Transcriber
""" Write a program that glues togehter the featuers of yt-dlp and Whisper to automatically download YouTube videos and produce subtitle files in the .srt format.
The input can be a list of URLs to download and transcribe. You can also add options to produce different subtitle formats. Python is an excellent "glue language" for
combining the capabilities of different modules. """

import subprocess 
import whisper 

url = input("YouTube URL: ") 

# Download audio
subprocess.run([ "yt-dlp", "-o", "video.mp4", url ], check=True) 

# Transcribe 
model = whisper.load_model("base") 
result = model.transcribe("audio.wav")

# Write SRT
write_function = whisper.utils.get_writer("srt", ".")
write_function(result, "audio")
