import logging

DEBUG_CODES = dict(d = logging.DEBUG,
                   w = logging.WARNING,
                   e = logging.ERROR,
                   i = logging.INFO,
                   x = logging.CRITICAL)

def get_debug_level(args):
    
    assert 1 <= len(args) <= 3
    if len(args) <= 2:
        return logging.CRITICAL
    else:
        assert len(args[2].split("-")) == 2
        assert args[2].split("-")[1] in ['d', 'w', 'e', 'i', 'x']
        debug_level = args[2].split("-")[1]

    return DEBUG_CODES[debug_level]

def get_user_info(args):

    assert len(args) > 1, "user info must be provided in form of 'btag-1234, pc, us'"
    inp = args[1]
    splits = inp.split(" ")
    btag = splits[0]
    system = splits[1]
    
    try:
        region = splits[2]
    except:
        region = None
    return btag, system, region 
