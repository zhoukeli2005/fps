# -*- coding: utf-8 -*-
#======================================================================
#
# packet.py - xxxx
#
#======================================================================

import struct

class packet(object):
    
    def __init__(self):
        self.__fmt = ">H"      # bigendian
        self.__value = [0]     # first element is SIZE of the packet
        
        self.__cache_fmt = ""
        self.__cache_pack = ""
        
    def __write(self, fmt, value):
        self.__fmt += fmt
        self.__value.append(value)
        
    def write_byte(self, b):
        self.__write("b", b)
    
    def write_ubyte(self, ub):
        self.__write("B", ub)
    
    def write_short(self, s):
        self.__write("h", s)
    
    def write_ushort(self, us):
        self.__write("H", us)
        
    def write_int(self, i):
        self.__write("i", i)
        
    def write_uint(self, ui):
        self.__write("I", ui)
        
    def write_float(self, f):
        self.__write("f", f)
        
    def write_string(self, str):
        self.__write(("%d" % len(str)) + "s", str)
        
    def pack(self):
        if(self.__fmt == self.__cache_fmt):
            return self.__cache_pack
        
        self.__value[0] = struct.calcsize(self.__fmt)
        
        self.__cache_fmt = self.__fmt;
        self.__cache_pack = struct.pack(self.__fmt, *self.__value)
        
        return self.__cache_pack
    
class read_packet(object):  
    def __init__(self, fmt):
        self.__fmt = ">H" + fmt
        self.__value = None
        self.__raw = ""
        self.__raw_len = struct.calcsize(self.__fmt)
        
    def unpack(self, raw):
        if len(raw) != self.__raw_len:
            print len(raw)
            print self.__raw_len
            raise Exception("read_packet.unpack error : no match!")
        
        if raw == self.__raw:
            return self.__value
        
        value = struct.unpack(self.__fmt, raw)
        self.__value = value[1:]
        return self.__value


if __name__ == '__main__':
    pkt = packet()
    pkt.write_byte(5)
    pkt.write_string("name")
    pkt.write_float(32.5)
    
    s = pkt.pack()
    print s.__repr__()
    
    rpkt = read_packet("b4sf")
    print rpkt.unpack(s)