# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:52:48 2018

@author: gasim500
"""

#SHELL Enter VI of Python 2.7
##activate "Python 2.7"

#SHELL Install needed libraries
##cd C:\Users\gasim500\Documents\VideoSubtitleExtraction\scripts
##pip install --upgrade google-cloud-speech

#SHELL Provide authentication credentials to your application code
##set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\gasim500\Documents\VideoSubtitleExtraction\Speech recognition project-abe688c48b3a.json


def transcribe_gcs(gcs_uri, output_filename):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
   
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
   # with open(output_filename, 'a+') as f:
   #     for result in response.results:
   #         # The first alternative is the most likely one for this portion.
   #         print(u'Transcript: {}'.format(result.alternatives[0].transcript))
   #         print('Confidence: {}'.format(result.alternatives[0].confidence))
   #         f.write(result.alternatives[0].transcript+" ")
    with open(output_filename, 'a+') as f:
        f.seek(0) #ensure you're at the start of the file..
        first_char = f.read(1) #get the first character
        if not first_char:
            for result in response.results:
                print(u'Transcript: {}'.format(result.alternatives[0].transcript))
                print('Confidence: {}'.format(result.alternatives[0].confidence))
                print("file is empty")
                f.write(result.alternatives[0].transcript+" ")
            else: pass
        
def main():
    filename = 'transcript.txt'
    gcs_input_uri = 'gs://aydanaudiofiles/monoaudio.wav'
    transcribe_gcs(gcs_input_uri, filename)
    
if __name__ == '__main__':
    main()

#manipulate the original text file to be the same format as the google output