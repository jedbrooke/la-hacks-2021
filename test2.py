import usb.core
import usb.util

def calcChecksum(inData):
    checksum = 0
    for inByte in inData:
        if type(inData) is list:
            inByte = int.from_bytes(inByte, byteorder='big')
        checksum = (((checksum & 0xFF) >> 1) + ((checksum & 0x1) << 7) + inByte) & 0xff
    return checksum

def main():

    dev = usb.core.find(idVendor = 0x04D8, idProduct = 0x8108)

    HEADER = (204).to_bytes(1, byteorder='big')
    TAIL = (185).to_bytes(1, byteorder='big')

    if dev is None:
        raise ValueError('Device not found')

    dev.set_configuration()

    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]

    ep = usb.util.find_descriptor(intf,
                                custom_match = \
                                lambda e: \
                                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                                    usb.util.ENDPOINT_OUT)

    assert ep is not None

    payload = 'test'

    message = bytearray()
    message += HEADER
    message += len(payload).to_bytes(1, byteorder='big')
    message += payload

    message += TAIL
    checksum = calcChecksum(payload)
    message += checksum.to_bytes(1, byteorder='big')
    message += bytes("\r\n".encode('ascii'))

    dev.write(message)