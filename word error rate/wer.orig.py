#!/usr/bin/env python
import sys
import numpy
import re
import os


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
	
def clean(what, afile, tofilename):
    # make sentence file
    content = '\n'.join(afile.read().split('\n\n'))
    content = re.sub('[\r\n]', '.\n', content)
    # remove anything within [] and ()
    content = re.sub(r'\[(.*?)\]|\((.*?)\)', '', content)
    content = re.sub('\s{2}', ' ', content)
    with open(tofilename, 'w') as sfile:
        sfile.write(content)

    # remove punctuation
    content = re.sub('[.,;:_+?!]', '', content.lower())

    # make a list
    alist = content.split()

    print('\n%s len: ' % what, len(alist), ' - ', alist[:10], '...', alist[-10:])
    return alist


# measure also WER per speaker


if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    debug = sys.argv[3]
    with open(filename1, 'r', encoding='utf-8') as file:
        r = clean('Reference', file, 'new_ref.txt')
    with open(filename2, 'r', encoding='utf-8') as file:
        h = clean('Hypothesis', file, 'new_hyp.txt')

    print('\nWER: ', wer(r, h))
    print('\nWER-Hunt: ', werH(r, h))
    
    os.remove('new_ref.txt')
    os.remove('new_hyp.txt')

if debug == 'True':
    print('\nReference: ', r)
    print('\nHypothesis: ', h)


# Credits and thanks to  https://martin-thoma.com/word-error-rate-calculation/
