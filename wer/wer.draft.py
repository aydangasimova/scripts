#!/usr/bin/env python
import sys
import numpy
import re
import os
#import itertools


def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 65535 elements (uint16).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    
    # initialisation
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint16)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion = d[i][j-1] + 1
                deletion = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"
    return result


def werH(r, h):
    # initialisation
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.float16)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion = d[i][j-1] + 0.5
                deletion = d[i-1][j] + 0.5
                d[i][j] = min(substitution, insertion, deletion)

    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"
    return result	  

def clean(input_filename):
    """
    :input_filename: input file name to read content from, string
    :out_file: file to write results
    :tmp_file: for some intermediate stuff
    """
    tmp_file='{}_tmp.txt'.format(input_filename)

        
# delete first 3 lines: this should only be the case if you are dealing with the reference file    
    if input_filename == referencefile_name:
        os.system("sed '1,3d' {} > {}".format(input_filename, tmp_file))
    else:
        os.system("cp {} {}".format(input_filename, tmp_file))
    
    with open(tmp_file, 'r+') as f_in:
        cleaned = ""
        for line in f_in:
            preprocessed_line = line.strip()
            
            if re.match('^\[\s?.+\s?\]$', preprocessed_line) is not None:
                preprocessed_line = ''
            
            if re.match('^\d\d:\d\d:\d\d.\d\d\d --> \d\d:\d\d:\d\d.\d\d\d', preprocessed_line) is not None:
                preprocessed_line = ''
                
            processed_line = preprocessed_line.replace('&gt;&gt', '')
            
            special_char = set('.,;:_+?!/\@#\\"$%^&*\'-=\"1234567890>♪')
            
            #if any((c in special_char) for c in processed_line):
            #    print("line contains special characters, cleaning line")
            processed_line = re.sub('[.,;:_+?!/\@#\\$%^&*\'-=\"1234567890>♪]', '', processed_line.lower())
            #else: 
            #    print("string contains NO special characters")
                
            if len(processed_line.strip()) > 0:
                cleaned += ' ' + processed_line
                

    os.system('rm {}'.format(tmp_file))
    
    return cleaned.strip()

# measure also WER per speaker
if __name__ == '__main__':
    referencefile_name = sys.argv[1]
    hypothesisfile_name = sys.argv[2]
    
    #debug mode
    #referencefile_name = "/home/aydan/Documents/Projects/stt_experiment/doc/references/vice_orig.vtt"
    #hypothesisfile_name = "/home/aydan/Documents/Projects/stt_experiment/doc/ocr/vice_ocr.txt"
    with open(referencefile_name, 'r', encoding='utf-8') as file:
        r = clean(referencefile_name)
    with open(hypothesisfile_name, 'r', encoding='utf-8') as file:
        h = clean(hypothesisfile_name)
    #print(h)
    #print(r)
    print('\nWER: ', wer(r.split(), h.split()))
    #print('\nWER-Hunt: ', werH(r_content.readlines(), h_content.readlines()))

print("system arguments are", sys.argv[1], sys.argv[2])

# Credits and thanks to  https://martin-thoma.com/word-error-rate-calculation/
