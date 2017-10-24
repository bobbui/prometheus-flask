
import time


def disk_writes_persec(sample_duration=1):
    """Return number of disk (reads, writes) per sec during the sample_duration."""
    num_writes1 = _disk_writes()
    time.sleep(sample_duration)
    num_writes2 = _disk_writes()
    writes_per_sec = (num_writes2 - num_writes1) / float(sample_duration)
    return writes_per_sec


def disk_reads_persec(sample_duration=1):
    """Return number of disk (reads, writes) per sec during the sample_duration."""
    num_reads1 = _disk_reads()
    time.sleep(sample_duration)
    num_reads2 = _disk_reads()
    reads_per_sec = (num_reads2 - num_reads1) / float(sample_duration)
    return reads_per_sec


def _disk_reads():
    num_reads = 0
    with open('/proc/diskstats') as f1:
        content = f1.read()
    for line in content.splitlines():
        fields = line.strip().split()
        num_reads += int(fields[3])

    return num_reads


def _disk_writes():
    num_writes = 0
    with open('/proc/diskstats') as f1:
        content = f1.read()
    for line in content.splitlines():
        fields = line.strip().split()
        num_writes += int(fields[7])
    return num_writes
