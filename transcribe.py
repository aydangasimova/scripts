# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:52:48 2018

@author: gasim500
"""

import sys


def transcribe_gcs(gcs_uri, output_filename, language):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
   
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code=language,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)

    for response in response.results:
        alternative = response.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))

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

print("it all seems to have worked")        

def main():
    gcs_uri = sys.argv[1]
    language = sys.argv[2]
    print(gcs_uri,language)
    filename = '{}-tscpt.txt'.format(gcs_uri[21:])
    transcribe_gcs(gcs_uri, filename, language)

if __name__ == '__main__':
    main()
