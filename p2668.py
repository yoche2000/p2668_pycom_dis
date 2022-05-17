import pycom
import network
from network import LoRa
import socket
import ubinascii
from dis_util import *

class P2668:
    def __init__(self):
        self.phy_dis, self.sen_dis  = csv_parse()       #Read DIS
        if(self.phy_dis["Radio"][1] == "0"):                 #Radio Type is Lora
            self.DevClass = self.phy_dis["DevClass"][1]
            self.adr = self.phy_dis["ADR"][1]
            self.Region = self.phy_dis["Region"][1]
            self.public = self.phy_dis["public"][1]

            if(self.phy_dis["Activation"][1] == "0"):                                   ##Store OTAA Keys
                self.Activation = '0'
                self.dev_eui = ubinascii.unhexlify(self.phy_dis["dev_eui"][1])
                self.app_eui = ubinascii.unhexlify(self.phy_dis["app_eui"][1])
                self.app_key = ubinascii.unhexlify(self.phy_dis["app_key"][1])
            elif(self.phy_dis["Activation"][1] == "1"):                                 ##Store ABP keys
                self.Activation = '1'
                self.dev_addr = ubinascii.unhexlify(self.phy_dis["dev_addr"][1])
                self.nwk_swkey = ubinascii.unhexlify(self.phy_dis["nwk_swkey"][1])
                self.app_swkey = ubinascii.unhexlify(self.phy_dis["app_swkey"][1])

            self.Fport = self.phy_dis["Fport"][1]

    def __str__(self):
        d = self.__dict__
        d.pop('sen_dis', None)
        d.pop('phy_dis', None)
        return(d)

    def get_phy_dis(self):                          #Print DIS
        """
        :get_phy_dis: Printing the Physical DIS of the P2668 object.
        """
        print("[SYS] Printing Physical DIS")
        print_dis(self.phy_dis)

    def get_sen_dis(self):
        """
        :get_phy_dis: Printing the Physical DIS of the P2668 object.
        """
        print("[SYS] Printing Sensor DIS")
        print_dis(self.sen_dis)

    def connect(self):

        reg_map = {'0':LoRa.AS923, '1':LoRa.AU915, '2':LoRa.EU868, '3':LoRa.US915, '4':LoRa.CN470, '5':LoRa.IN865}
        p = True if self.public == '1' else False
        a = True if self.adr == '1' else False
        lora = LoRa(mode=LoRa.LORAWAN, adr=a, public=p, tx_retries=1000, region=reg_map[self.Region])

        if (self.Activation == '0'):
            auth = (self.dev_eui, self.app_eui, self.app_key)
            lora.join(activation=LoRa.OTAA, auth=auth, timeout = 0)
            print("[LOR] Joined Request Sent")

            pycom.heartbeat(False)
            pycom.rgbled(0x7f0000)

            while not lora.has_joined():
                time.sleep(1)
                print('[LOR] Not yet joined ')
            print("[LOR] Joined")
            pycom.heartbeat(True)

            self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
            self.socket.setblocking(False)
            self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
            self.socket.bind(int(self.Fport))
            print("[LOR] Socket Created: " + str(self.socket))
