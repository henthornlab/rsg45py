from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT
import struct

rsg_path = '10.64.0.61'

with CIPDriver(rsg_path) as rsg:
    
    print('Reading config from RSG')
    param = rsg.generic_message(
        service=Services.get_attribute_single,
        class_code=4,
        instance=5,  # Config Assembly
        attribute=3,
        connected=True,
        unconnected_send=True,
    )


    if (param.error == None):
        print('Successfully read from device')
    else:
        print('Error message was ', param.error)
    
    config_bytes = bytearray(398)
    
    config_bytes[6] = 0x11
    config_bytes[7] = 0x10
    config_bytes[8] = 0x21
    config_bytes[9] = 0x10
    config_bytes[10] = 0x31
    config_bytes[11] = 0x10
    config_bytes[12] = 0x41
    config_bytes[13] = 0x10
    config_bytes[14] = 0x51
    config_bytes[15] = 0x10
    config_bytes[16] = 0x61
    config_bytes[17] = 0x10

    print('Writing new config to device')
    setconfig_msg = rsg.generic_message(
        service=Services.set_attribute_single,
        class_code=4,
        instance=5,  # Config Assembly
        attribute=3,
        connected=True,
        unconnected_send=True,
        request_data=bytes(config_bytes)
    )

    if (setconfig_msg.error == None):
        print('Successfully wrote to the device')
    else:
        print('Error message when writing new config ', setconfig_msg.error)

    print('Checking values and status -- Instance 100')

    param = rsg.generic_message(
        service=Services.get_attribute_single,
        class_code=4,
        instance=100,  # Config Assembly
        attribute=3,
        connected=True,
        unconnected_send=True,
    )

    vals = bytearray(param.value)


    print('Values are:')
    print(struct.unpack('f', vals[56:60]))
    print(struct.unpack('f', vals[60:64]))
    print(struct.unpack('f', vals[64:68]))
    print(struct.unpack('f', vals[68:72]))
    print(struct.unpack('f', vals[72:76]))
    print(struct.unpack('f', vals[76:80]))




