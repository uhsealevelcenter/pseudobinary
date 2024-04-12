
import struct
import binascii

def pb2dec(b):
    bits = len(b) * 6
    yy = ''
    for d in range(0,len(b)):
        dd = ord(b[d])
        if dd > 63 : dd -= 64
        yy += bin(dd)[2:].zfill(6)
    val = int(yy,2)
    # compute the 2's complement of int value val
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

class pseudobinary:
    def __init__(self,data = None):
        self.load(data)

    def load(self,data):
        self.entire_msg = data
        self.unpack()

    def unpack(self):
        bar = []
        if self.entire_msg:
            l = len(self.entire_msg)
            #nmsg = self.entire_msg.count('+')
            m = self.entire_msg
        else:
            self.block_identifier = 'Z'

        self.block_identifier   = m[0]     # type is B, 2, C, or D

        # this isnt right anymore because type2 random from above doesnt have a m[1]
        # self.group_id           = m[1]     # 1=scheduled, 2=alarm, 3=forced, 4=retx

        # print(len(vals))
        # Message block
        # for d in range(0,int(len(vals)/3)):

        if self.block_identifier == 'B':
            self.group_id           = m[1]     # 1=scheduled, 2=alarm
            self.offset = pb2dec(m[2])
            msgs = m[3:-1]
            nmsg = len(msgs)/3
#            print(nmsg)
#            for msg in range(1,int(nmsg+1)):
            #print(msgs)
            for i in range(0,int(nmsg)):
#                 print('BT' + str(msg))
                 msg = msgs[i*3:(i*3)+3]
                 bar.append(pb2dec(msg))
            self.random_count = 0

# 2ANr}SGI
        if self.block_identifier == '2':
            self.group_id           = 6     # 6=random
            self.offset = pb2dec(m[1])
            msgs = m[2:-3]
            nmsg = len(msgs)/3
            #print(msgs)
            for i in range(0,int(nmsg)):
                 msg = msgs[i*3:(i*3)+3]
                 bar.append(pb2dec(msg))
            rcnt = m[-3:-1]
            # print(rcnt)
            self.random_count = pb2dec(rcnt)


        if self.block_identifier == 'C':
            self.group_id           = m[1]     # 1=scheduled, 2=alarm, 3=forced, 4=retx
            # All the sensor data 
            msgs = m[2:-2].split('+')
            nmsg = self.entire_msg.count('+')
            for msg in range(1,nmsg+1):
#                 print(msgs[msg])
#                 print(decodePBC(msgs[msg]))
                 bar.append(decodePBC(msgs[msg]))
            self.random_count = 0

        self.batt           = pb2dec(m[-1])*0.234+10.6      # battery voltage
        self.data = bar
#        print(bar)

def decodePBB(c):
    y = []
    vals = c
    for d in range(0,int(len(vals)/3)):
        y.append(pb2dec(vals[d*3:d*3+3]))
    return y
 

def decodePBC(c):
    y = []
    y.append(pb2dec(c[0]))   # index
    y.append(pb2dec(c[1:3])) # jd
    y.append(pb2dec(c[3:5])) # min of day
    y.append(pb2dec(c[5:7])) # sensor interval
    vals = c[7:]
#    print (vals)
    for d in range(0,int(len(vals)/3)):
        y.append(pb2dec(vals[d*3:d*3+3]))
    return y


def testjig():

    testmsg = 'C1+ACPA]@A@SR@SR@SR@SR@SR+BCPA]@A@di@di@di@di@di+CCPA\@E@v@+DCP@|@|+ECPAZ@|@@|+FCPAY@O@Ax.L'
    testmsg = 'C1+ACP@~@A@SR@SR@SR@SR+BCP@~@A@di@di@di@di+CCP@~@E@v@+DCP@|@|@@@+ECP@^@|+FCP@{@O@Ax.K'
    testmsg = 'B1@@Gt@Gs@Sx@Sr@@i@@iI'
    testmsg = 'B1A@^k@^k@^i@^h@^i@^h@^g@^g@^i@^g@^d@^d@^d@^e@^b@^d@^d@^b@^`@^b@^c@^_@^_@^aH'
    testmsg = 'C1+ACPA]@A@SR@SR@SR@SR@SR+BCPA]@A@di@di@di@di@di+CCPA\@E@v@+DCP@|@|+ECPAZ@|@@|+FCPAY@O@Ax.L'
    testmsg = 'C1+ABqKP@E@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR@SR.'
    testmsg = r'B1B@\o@\p@\r@\t@\t@\v@\x@\z@\|@\}@\?@]A@]C@]D@]F@]H@]J@]K@]M@]O@]P@]R@]T@]VI'
    testmsg = 'B1B@VF@VG@VG@VH@VH@VI@VI@VJ@VJ@VJ@VK@VK@VK@VL@VL@VM@VM@VM@VN@VN@VN@VO@VO@VOI'

    M = pseudobinary(testmsg)
#    M.unpack()

#    print('orig msg: ' + testmsg)
    print(M.block_identifier)
#    print(M.msg_delimiter)
#    print(M.measurement_index)
#    print(M.msg_day)
#    print(M.msg_time)
#    print(M.msg_interval)
    print(M.data)
    print(M.batt)


# == MAIN ==
if __name__ == '__main__':
    testjig()


