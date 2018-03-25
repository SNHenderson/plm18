def keyvalues(d):
    """Return a string of the dictionary,
       keys in sorted order,
       hiding any key that starts with '_'"""
    return '(' + ', '.join(['%s: %s' % (k, d[k])
                            for k in sorted(d.keys())
                            if k[0] != "_"]) + ')'
class dict_obj(object):
    def __init__(self, **dic):
        self.__dict__.update(dic)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return self.__class__.__name__ + keyvalues(self.__dict__)
