
def isBirthyear(s):
    if (s.find('род.') > 0)
        return s[5:4:1]
    return -1

def isArea(s):
    r = s.find('обл.') if (s.find('обл.') > - 1) else s.find('обл')
    if (r > 0):
        return s[0:r-1:1]
    return -1