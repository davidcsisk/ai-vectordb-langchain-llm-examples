import os, sys
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

if len(sys.argv) == 1:
    print("Pass in the audio filename")
    quit()

file_name = sys.argv[1]

with open(file_name, "rb") as audio_file:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    
    