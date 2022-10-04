import hashlib

import wmi

class register:
    def __init__(self):
       self.getCombinNumber()

    #  1. 获取硬件信息,输出 macode
    #  1.CPU序列号（ID） 2.本地连接 无线局域网 以太网的MAC 3.硬盘序列号（唯一） 4.主板序列号（唯一）

    global s
    s = wmi.WMI()

    # cpu 序列号
    def get_CPU_info(self):
        cpu = []
        cp = s.Win32_Processor()
        for u in cp:
            cpu.append(
                {
                    "Name": u.Name,
                    "Serial Number": u.ProcessorId,
                    "CoreNum": u.NumberOfCores
                }
            )
        return cpu

    # 硬盘序列号
    def get_disk_info(self):
        disk = []
        for pd in s.Win32_DiskDrive():
            disk.append(
                {
                    "Serial": s.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),  # 获取硬盘序列号，调用另外一个win32 API
                    "ID": pd.deviceid,
                    "Caption": pd.Caption,
                    "size": str(int(float(pd.Size) / 1024 / 1024 / 1024)) + "G"
                }
            )
        return disk

    # mac 地址（包括虚拟机的）
    def get_network_info(self):
        network = []
        for nw in s.Win32_NetworkAdapterConfiguration():  # IPEnabled=0
            if nw.MACAddress != None:
                network.append(
                    {
                        "MAC": nw.MACAddress,  # 无线局域网适配器 WLAN 物理地址
                        "ip": nw.IPAddress
                    }
                )
        return network

    # 主板序列号
    def get_mainboard_info(self):
        mainboard = []
        for board_id in s.Win32_BaseBoard():
            mainboard.append(board_id.SerialNumber.strip().strip('.'))
        return mainboard

    #  由于机器码太长，故选取机器码字符串部分字符

    #  74:4C:A1:9D:94:0A178BFBFF00A50F0000A0_7501_2D69_E09C.PF2ZDT23
    #                  A              0   A  7     D   E

    def getCombinNumber(self):
        a = self.get_network_info()
        b = self.get_CPU_info()
        c = self.get_disk_info()
        d = self.get_mainboard_info()
        machinecode_str = ""
        machinecode_str = machinecode_str + a[0]['MAC'] + b[0]['Serial Number'] + c[0]['Serial'] + d[0]
        selectindex = [16,2, 31,18,18, 34, 38, 44, 48]
        macode = "刘杨"
        for i in selectindex:  # 根据字符串位数筛选部分字符
            macode = macode + machinecode_str[i]
        macode=macode+'1024839103'
        MD5 = hashlib.md5()
        MD5.update(macode.encode(encoding='utf-8'))
        return MD5.hexdigest()


