from scapy.all import *
from dofus_packet import DofusPacket
from rune import Rune
from item import Item
from display import Display
import binascii

filter = "host 213.248.126.61"

display = Display()

rune = None
item = None

def handle(pkt):
    if pkt[IP].len > 40:
        try:
            pktdata = pkt[Raw].load
            while True:
                pktdata, extracted = pop_pkt(pktdata)
                if extracted.isInteresting():

                    display.test(extracted.id)
                    parsed_packet = extracted.parse()
                    print(parsed_packet)

                    if parsed_packet['type'] == 'rune':
                        rune = Rune(parsed_packet['data']['objectGID'], display)

                    elif parsed_packet['type'] == 'item':
                        item = Item(parsed_packet['data']['objectGID'], display)
                        item.initLinesUsingPacket(parsed_packet)

                if len(pktdata) <= 2:
                    break

        except IndexError:
            pass


def get_pkt_id(pkt):
    oct0 = pkt[0]
    oct1 = (pkt[1] & 0b11111100)//4
    return oct1 + oct0*64

def get_data_len_len(pkt):
    return pkt[1] & 0b00000011

def get_data_len(pkt, len_len):
    return (int.from_bytes(pkt[2:2+len_len], byteorder='big'))

def get_data(pkt, len_len, data_len):
    return(pkt[2+len_len:2+len_len+data_len])

def pop_pkt(pkt):
    id = get_pkt_id(pkt)
    data_len_len = get_data_len_len(pkt)
    data_len = get_data_len(pkt, data_len_len)
    data = get_data(pkt, data_len_len, data_len)
    extracted = DofusPacket(id, data_len, data)
    remaining = pkt[2+data_len_len+data_len:]
    return(remaining, extracted)

# ------ START SNIFFER
sniff(store=0, filter=filter, prn=handle)
