import numpy as np
import pyfits
import pywcs

def sip2idc(wcs):
    """
    Converts SIP style coefficients to IDCTAB coefficients.
    
    :Parameters:
    `wcs`: pyfits.Header or pywcs.WCS object
    """
    if isinstance(wcs,pyfits.Header):
        ocx10 = wcs.get('OCX10', None)
        ocx11 = wcs.get('OCX11', None)
        ocy10 = wcs.get('OCY10', None)
        ocy11 = wcs.get('OCY11', None)
        order = hdr.get('A_ORDER', None)
        sipa, sipb = _read_sip_kw(header)
        if sipa == None or sipb == None:
            print 'SIP coefficients are not available.\n'
            print 'Cannot convert SIP to IDC coefficients.\n'
            return
    elif isinstance(wcs,pywcs.WCS):
        try:
            ocx10 = wcs.ocx10
            ocx11 = wcs.ocx11
            ocy10 = wcs.ocy10
            ocy11 = wcs.ocy11
        except AttributeError:
            print 'First order IDCTAB coefficients are not available.\n'
            print 'Cannot convert SIP to IDC coefficients.\n'
            return
        try:
            sipa = wcs.sip.a
            sipb = wcs.sip.b
        except AttributeError:
            print 'SIP coefficients are not available.\n'
            print 'Cannot convert SIP to IDC coefficients.\n'
            return
    else:
        print 'Input to sip2idc must be a PyFITS header or a wcsutil.HSTWCS object\n'
        return
    
    try:
        order = wcs.sip.a_order
    except AttributeError:
        print 'SIP model order unknown, exiting ...\n'
        return

    if None in [ocx10, ocx11, ocy10, ocy11]:
        print 'First order IDC coefficients not found, exiting ...\n'
        return
    idc_coeff = np.array([[ocx11, ocx10], [ocy11, ocy10]])
    cx = np.zeros((order+1,order+1), dtype=np.double)
    cy = np.zeros((order+1,order+1), dtype=np.double)
    for n in range(order+1):
        for m in range(order+1):
            if n >= m and n>=2:
                sipval = np.array([[sipa[m,n-m]],[sipb[m,n-m]]])
                idcval = np.dot(idc_coeff, sipval)
                cx[n,m] = idcval[0]
                cy[n,m] = idcval[1]
    
    cx[1,0] = ocx10
    cx[1,1] = ocx11
    cy[1,0] = ocy10
    cy[1,1] = ocy11
                
    return cx, cy

def _read_sip_kw(header):
    """
    Reads SIP header keywords and returns an array of coefficients.

    If no SIP header keywords are found, None is returned.
    """
    if header.has_key("A_ORDER"):
        if not header.has_key("B_ORDER"):
            raise ValueError(
                "A_ORDER provided without corresponding B_ORDER "
                "keyword for SIP distortion")

        m = int(header["A_ORDER"])
        a = np.zeros((m+1, m+1), np.double)
        for i in range(m+1):
            for j in range(m-i+1):
                a[i, j] = header.get("A_%d_%d" % (i, j), 0.0)

        m = int(header["B_ORDER"])
        b = np.zeros((m+1, m+1), np.double)
        for i in range(m+1):
            for j in range(m-i+1):
                b[i, j] = header.get("B_%d_%d" % (i, j), 0.0)
    elif header.has_key("B_ORDER"):
        raise ValueError(
            "B_ORDER provided without corresponding A_ORDER "
            "keyword for SIP distortion")
    else:
        a = None
        b = None
            
    return a , b
"""
def idc2sip(wcsobj, idctab = None):
    if isinstance(wcs,pywcs.WCS):
        try:
            cx10 = wcsobj.ocx10
            cx11 = wcsobj.cx11
            cy10 = wcsobj.cy10
            cy11 = wcsobj.cy11
        except AttributeError:
            print 
        try:
            order = wcs.sip.a_order
        except AttributeError:
            print 'SIP model order unknown, exiting ...\n'
            return
    else:
        print 'Input to sip2idc must be a PyFITS header or a wcsutil.HSTWCS object\n'
        return
    
    if None in [ocx10, ocx11, ocy10, ocy11]:
        print 'First order IDC coefficients not found, exiting ...\n'
        return
    idc_coeff = np.array([[wcsobj.cx11, wcsobj.cx10], [wcsobj.cy11, wcsobj.cy10]])
    cx = numpy.zeros((order+1,order+1), dtype=numpy.double)
    cy = numpy.zeros((order+1,order+1), dtype=numpy.double)
    for n in range(order+1):
        for m in range(order+1):
            if n >= m and n>=2:
                sipval = numpy.array([[wcsobj.sip.a[n,m]],[wcsobj.sip.b[n,m]]])
                idcval = numpy.dot(idc_coeff, sipval)
                cx[m,n-m] = idcval[0]
                cy[m,n-m] = idcval[1]
                
    return cx, cy
"""