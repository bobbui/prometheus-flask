import psutil


def rx_tx_bytes(interface):
    for line in open('/proc/net/dev'):
        if interface in line:
            data = line.split('%s:' % interface)[1].split()
            rx_bytes, tx_bytes = (int(data[0]), int(data[8]))
            return (rx_bytes, tx_bytes)
    raise NetError('interface not found: %r' % interface)


class NetError(Exception):
    pass

