#http://code.google.com/p/pypng/source/browse/trunk/code/png.py

# Conditionally convert to bytes.  Works on Python 2 and Python 3.
try:
    bytes('', 'ascii')
    def strtobytes(x): return bytes(x, 'iso8859-1')
    def bytestostr(x): return str(x, 'iso8859-1')
except:
    strtobytes = str
    bytestostr = str

def read_pnm_header(infile, supported=('P5','P6')):
    """
    Read a PNM header, returning (format,width,height,depth,maxval).
    `width` and `height` are in pixels.  `depth` is the number of
    channels in the image; for PBM and PGM it is synthesized as 1, for
    PPM as 3; for PAM images it is read from the header.  `maxval` is
    synthesized (as 1) for PBM images.
    """

    # Generally, see http://netpbm.sourceforge.net/doc/ppm.html
    # and http://netpbm.sourceforge.net/doc/pam.html

    supported = [strtobytes(x) for x in supported]

    # Technically 'P7' must be followed by a newline, so by using
    # rstrip() we are being liberal in what we accept.  I think this
    # is acceptable.
    type = infile.read(3).rstrip()
    #if type not in supported:
    #    raise NotImplementedError('file format %s not supported' % type)
    if type == strtobytes('P7'):
        # PAM header parsing is completely different.
        return read_pam_header(infile)
    # Expected number of tokens in header (3 for P4, 4 for P6)
    expected = 4
    pbm = ('P1', 'P4')
    if type in pbm:
        expected = 3
    header = [type]

    # We have to read the rest of the header byte by byte because the
    # final whitespace character (immediately following the MAXVAL in
    # the case of P6) may not be a newline.  Of course all PNM files in
    # the wild use a newline at this point, so it's tempting to use
    # readline; but it would be wrong.
    def getc():
        c = infile.read(1)
        if not c:
            raise Exception('premature EOF reading PNM header')
        return c

    c = getc()
    while True:
        # Skip whitespace that precedes a token.
        while c.isspace():
            c = getc()
        # Skip comments.
        while c == '#':
            while c not in '\n\r':
                c = getc()
        if not c.isdigit():
            print('unexpected character %s found in header' % c)
            raise Exception('unexpected character %s found in header' % c)
        # According to the specification it is legal to have comments
        # that appear in the middle of a token.
        # This is bonkers; I've never seen it; and it's a bit awkward to
        # code good lexers in Python (no goto).  So we break on such
        # cases.
        token = strtobytes('')
        while c.isdigit():
            token += c
            c = getc()
        # Slight hack.  All "tokens" are decimal integers, so convert
        # them here.
        header.append(int(token))
        if len(header) == expected:
            break
    # Skip comments (again)
    while c == '#':
        while c not in '\n\r':
            c = getc()
    if not c.isspace():
        raise Exception('expected header to end with whitespace, not %s' % c)

    if type in pbm:
        # synthesize a MAXVAL
        header.append(1)
    depth = (1,3)[type == strtobytes('P6')]
    return header[0], header[1], header[2], depth, header[3]
