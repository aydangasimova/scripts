import numpy

def wer(r, h, backtracking=False):
    """
    Calculation of WER with Levenshtein distance. Existing code is extended with backtracking.

    O(nm) time ans space complexity.

    Parameters
    ----------
    r : string
    h : string
    backtracking : boolean for backtracking

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there", "is there")
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    r = r.split()
    h = h.split()
    # initialisation
    d = numpy.zeros((len(r) + 1, len(h) + 1))
    backtrace = numpy.zeros(d.shape)
    # Backtrace mapping 0 = Substition, 1 = Insertion, 2 = Deletition, 3=OK

    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
                backtrace[i][j] = 3
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

                if backtracking:
                    if d[i][j] == substitution:
                        backtrace[i][j] = 0
                    elif d[i][j] == insertion:
                        backtrace[i][j] = 1
                    else:
                        backtrace[i][j] = 2

    if backtracking:
        i = len(r)
        j = len(h)
        num_sub = 0
        num_ok = 0
        num_ins = 0
        num_del = 0
        debug = True
        lines = []
        print('\t Truth \t\t Hypo')
        while i > 0 or j > 0:
            if i == 0:
                j -= 1
                num_ins += 1
                if debug:
                    lines.append("INS\t" + "****" + "\t" + h[j])
            elif j == 0:
                i -= 1
                num_del += 1
                if debug:
                    lines.append("DEL\t" + "****" + "\t" + h[j])
            elif backtrace[i][j] == 3:
                backtrace[i][j] = 93
                num_ok += 1
                i -= 1
                j -= 1
                if debug:
                    lines.append("OK\t" + r[i] + "\t" + h[j])
            elif backtrace[i][j] == 0:
                backtrace[i][j] = 90
                num_sub += 1
                i -= 1
                j -= 1
                if debug:
                    lines.append("SUB\t" + r[i] + "\t" + h[j])
            elif backtrace[i][j] == 1:
                backtrace[i][j] = 91
                num_ins += 1
                j -= 1
                if debug:
                    lines.append("INS\t" + "****" + "\t" + h[j])
            elif backtrace[i][j] == 2:
                backtrace[i][j] = 92
                num_del += 1
                i -= 1
                if debug:
                    lines.append("DEL\t" + r[i] + "\t" + "****")

        lines = reversed(lines)
        for line in lines:
            print(line)
        print("#correct " + str(num_ok))
        print("#sub " + str(num_sub))
        print("#del " + str(num_del))
        print("#ins " + str(num_ins))

    # return d[len(r)][len(h)]
    return round(d[len(r)][len(h)] / float(len(r)), 4)