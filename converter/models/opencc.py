from enum import Enum


class OpenCCModel(str, Enum):
    hk2s = "hk2s.json"
    s2hk = "s2hk.json"
    s2t = "s2t.json"
    s2tw = "s2tw.json"
    s2twp = "s2twp.json"
    t2s = "t2s.json"
    tw2s = "tw2s.json"
    tw2sp = "tw2sp.json"
    t2tw = "t2tw.json"
    t2hk = "t2hk.json"
