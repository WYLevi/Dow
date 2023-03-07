import socket
import numpy as np
import configparser
import time
import keyboard


class PLC:
    def __init__(self):
        self.responseM266 = "8000000"
        self.responseX006 = "8000000"
        self.responseX110 = "8000000"
        self.responseM507 = "8000010"
        self.reload_plc_config()
        if self.status == "prod":
            # self.client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   #UDP
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            self.client.connect((self.host, self.port))  ###PLC Test

    def reload_plc_config(self):
        ###PLC端資訊
        parser = configparser.ConfigParser()
        parser.read("./cfg/setting.cfg")
        ### section names
        source = parser["Source"]
        reg1 = parser["Reg_1"]
        reg2 = parser["Reg_2"]
        reg3 = parser["Reg_3"]
        reg4 = parser["Reg_4"]
        reg5 = parser["Reg_5"]
        reg6 = parser["Reg_6"]
        ### PLC host = "192.168.1.3"
        self.host = source["host"]
        self.port = int(source["port"])
        self.status = source["status"]
        ### Read Register
        self.startReg1 = reg1["startReg"]
        self.startReg2 = reg2["startReg"]
        self.startReg3 = reg3["startReg"]
        self.startReg4 = reg4["startReg"]
        self.startReg5 = reg5["startReg"]
        self.startReg6 = reg6["startReg"]
        self.length1 = reg1["length"]
        self.length2 = reg2["length"]
        self.length3 = reg3["length"]
        self.length4 = reg4["length"]
        self.length5 = reg5["length"]
        self.length6 = reg6["length"]

    def get(self, afterValue: int, register: str, startNum: int, devicePoints: int, dataType="bit", format="binary"):
        ### FX3U-ENET-L -> 1word = 2Bytes = 16bits
        if dataType == "bit":  # X、Y、M、S、T、C
            subheader = bytearray(b"\x00")
        elif dataType == "word":  # X、Y、M、S、T、C(16bits) / D、R、T、C(1bit)
            subheader = bytearray(b"\x01")
        ### register name
        startNumOrg = startNum
        register = register.upper()
        if register == "D":
            deviceName = bytearray(b"\x44\x20")
        elif register == "M":
            deviceName = bytearray(b"\x4D\x20")
        elif register == "X":  # X start number is octal
            deviceName = bytearray(b"\x58\x20")
            startNum = int("0o" + str(startNum), 8)  # octal to decimal
        else:
            raise Exception("Does not support register type " + str(register) + ".")
        ### 起始位址 & 暫存器點數定義 & 監控定時器
        PCNum = bytearray(b"\xFF")
        monitorTime = bytearray(b"\x00\x0A")
        startNum = int(startNum).to_bytes(4, "little")  # little:L>H, big:H>L
        devicePoints = int(devicePoints).to_bytes(1, "little")
        endCode = bytearray(b"\x00")
        ### 2進制格式(12): 副標(1) / PC號(1) / 監控定時器(L>H:2) / 起始元件(L>H:4) / 元件名(L>H:2) / 元件點數(1) /結束碼(1)
        if format == "binary":
            msg = subheader + PCNum + monitorTime[::-1] + startNum + deviceName[::-1] + devicePoints + endCode
        elif format == "ASCII":
            print("TBD")
        ### send the command to PLC
        time.sleep(0.001)
        # print(f"read command: {msg.hex()}")
        if self.status == "prod":
            self.client.send(msg)  ###PLC Test
            ## response from PLC  ###PLC Test
            response = self.client.recv(1024)
            responseHex = response.hex()
            responseEndcode = responseHex[2:4]
            ##error code process  ###PLC Test
            if responseEndcode != "00":
                print(f"【Response Error】Reg.:{register}{startNum}, Endcode:{responseEndcode}")  # TODO:需加進log
            ##PLC Test
            if startNumOrg == 266:
                if afterValue == 1 and responseHex[-2] == 1:
                    responseHex = "8000010"
            return responseHex
        else:
            if startNumOrg == 266:
                if afterValue == 1:
                    self.responseM266 = "8000010"
                if keyboard.is_pressed("w"):
                    self.responseM266 = "8000000"
                elif keyboard.is_pressed("s"):
                    self.responseM266 = "8000010"
                return self.responseM266

            elif startNumOrg == 6:
                if keyboard.is_pressed("e"):
                    self.responseX006 = "8000000"
                elif keyboard.is_pressed("d"):
                    self.responseX006 = "8000010"
                return self.responseX006

            elif startNumOrg == 110:
                if keyboard.is_pressed("r"):
                    self.responseX110 = "8000000"
                elif keyboard.is_pressed("f"):
                    self.responseX110 = "8000010"
                return self.responseX110

            elif startNumOrg == 507:
                if keyboard.is_pressed("x"):
                    self.responseM507 = "8000000"
                elif keyboard.is_pressed("o"):
                    self.responseM507 = "8000010"
                return self.responseM507

    def set(self, value: str, register: str, startNum: int, devicePoints: int, dataType="bit", format="binary"):
        ### set value (input must be list type)
        # value = np.array([value])
        ### FX3U-ENET-L -> 1word = 2Bytes = 16bits
        data = bytearray()
        temp = bytearray()
        if dataType == "bit":  # X、Y、M、S、T、C
            subheader = bytearray(b"\x02")
            value = str(value)  # the bit value must be 0 or 1
            if len(value) % 2 != 0:
                print("【ERROR】value must be even!")
            bytes.fromhex(value)
            for i in range(len(value) // 2):  # bit format
                if value[0 + 2 * i : 2 + 2 * i] == "00":
                    temp = b"\x00"
                elif value[0 + 2 * i : 2 + 2 * i] == "01":
                    temp = b"\x01"
                elif value[0 + 2 * i : 2 + 2 * i] == "10":
                    temp = b"\x10"
                elif value[0 + 2 * i : 2 + 2 * i] == "11":
                    temp = b"\x11"
                data += temp
        elif dataType == "word":  # Y、M、S、T、C(16bits) / D、R、T、C(1bit)
            subheader = bytearray(b"\x03")
            for v in value:
                temp = int(v).to_bytes(2, "little")  # little:L>H, big:H>L
                data += temp
        ### register name
        register = register.upper()
        if register == "D":
            deviceName = bytearray(b"\x44\x20")
        elif register == "M":
            deviceName = bytearray(b"\x4D\x20")
        elif register == "X":
            deviceName = bytearray(b"\x58\x20")
            startNum = int("0o" + str(startNum), 8)  # octal to decimal
        else:
            raise Exception("Does not support register type " + str(register) + ".")
        ### 起始位址 & 暫存器點數定義 & 監控定時器
        PCNum = bytearray(b"\xFF")
        monitorTime = bytearray(b"\x00\x0A")
        startNum = int(startNum).to_bytes(4, "little")
        devicePoints = int(devicePoints).to_bytes(1, "little")
        endCode = bytearray(b"\x00")
        ### 2進制格式(12): 副標(1) / PC號(1) / 監控定時器(L>H:2) / 起始元件(L>H:4) / 元件名(L>H:2) / 元件點數(1) /結束碼(1) / data
        if format == "binary":
            msg = subheader + PCNum + monitorTime[::-1] + startNum + deviceName[::-1] + devicePoints + endCode + data
        elif format == "ASCII":
            print("TBD")
        ### send the command to PLC ###PLC Test
        if self.status == "prod":
            self.client.send(msg)
        ### response from PLC ###PLC Test
        # response = self.client.recv(1024)
        # print(f"write response:{response.hex()}")

        time.sleep(0.001)
        return msg.hex()

    def stop(self):
        self.client.shutdown
        self.client.close


if __name__ == "__main__":

    parser = configparser.ConfigParser()
    parser.read("./cfg/setting.cfg")
    ### section names
    __source = parser["Source"]
    __read1 = parser["Read_1"]
    __read2 = parser["Read_2"]
    __write = parser["Write"]
    ### PLC host = "192.168.1.3"
    host = __source["host"]
    port = int(__source["port"])
    ### Read Register
    readReg1 = __read1["startReg"]
    readReg2 = __read2["startReg"]
    readLength1 = __read1["length"]
    readLength2 = __read2["length"]
    ### write Register
    writeReg = __write["startReg"]
    writeLength = __write["length"]
    value = __write["value"]
    print(f"PLC IP: {host}:{port}")
    print(f"Read Registers: {readReg1}, {readReg2}")
    PLCObject = PLC(host, port)

    while True:
        try:
            ### bit(R:00/W:02), word(R:01/W:03)
            responseData1 = PLCObject.get(
                register=readReg1[0],
                startNum=int(readReg1[1:]),
                devicePoints=readLength1,
                dataType="bit",
                format="binary",
            )
            print(f"1.Read {readReg1}, Response: {responseData1}")

            responseData2 = PLCObject.get(
                register=readReg2[0],
                startNum=int(readReg2[1:]),
                devicePoints=readLength2,
                dataType="bit",
                format="binary",
            )
            print(f"2.Read {readReg2}, Response: {responseData2}")

            PLCObject.set(
                value=value,
                register=writeReg[0],
                startNum=int(writeReg[1:]),
                devicePoints=writeLength,
                dataType="bit",
                format="binary",
            )
            responseData3 = PLCObject.get(
                register=readReg2[0],
                startNum=int(readReg2[1:]),
                devicePoints=readLength2,
                dataType="bit",
                format="binary",
            )
            print(f"3.Read {readReg2}, Response: {responseData2}")
            time.sleep(3000)

        except:
            print("in except condition...")
