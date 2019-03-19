# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:55:18 2018

@author: gasim500
"""

gcloud config list
gcloud ml speech

#extract audio from video file and store it in an wav file
ffmpeg -i VOexCpTHxLI_en_embedded.mp4 -f wav -vn audio.wav

#slice video piece
ffmpeg -ss 00:00:00.0 -i audio.wav -c copy -t 00:00:10.0 slicedaudio.wav

#modify audio file channels into a mono sound only
ffmpeg -i slicedaudio.wav -ac 1 monoslicedaudio.wav
ffmpeg -i audio.wav -ac 1 monoaudio.wav

#run gcloud speech recognition command
gcloud ml speech recognize  monoslicedaudio.wav --language-code=en-US

#this is a good start but we can already see the output is not matching what the man says in the audio. Also note the confidence score reported. Speculatively, it could be due to his accent..

#since for our WER analysis we want to examine the entire length of the video, we want to find a way to split the audio into largest possible parts, run the speech recognition command on each separately and then combine the output into one text file.

#for this you will need to follow suggested steps in google SDK console to install alpha components
gcloud alpha ml speech recognize-long-running monoaudio.wav --language-code=en-US

#create a bucket on cloud storage first - called aydanaudiofiles and then run it through the cloud directly because there is a bug when trying to run it locally
gcloud alpha ml speech recognize-long-running gs://aydanaudiofiles/monoaudio.wav --language-code=en-US

#we can see the transcription is appearing in chunks, why is that? Does the api recognize the different speakers?

#assumption: possibly due to the fact that the transcription happens synchronously, chunks are spitted out

#need to figure out how to use the curl config part of the function to tailor the code

gcloud alpha ml speech recognize-long-running gs://aydanaudiofiles/monoaudio.wav --language-code=en-US --include-word-time-offsets --format=json --enable_speaker_diarization=True





#next step is to parse the JSON output for the transcript and use it to calculate the WER against the subtitle file.


#The following Python code iterates over a result list and concatenates the transcriptions together. Note that we take the first alternative (the zeroth) in all cases.


response = service_request.execute()
recognized_text = 'Transcribed Text: \n'
for i in range(len(response['results'])):
    recognized_text += response['results'][i]['alternatives'][0]['transcript']
    
    
