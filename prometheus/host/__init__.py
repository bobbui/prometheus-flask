# coding=utf-8
import multiprocessing
from _curses import has_key

import netifaces

import psutil
from prometheus.host.linux import net_stat, disk_stat
from prometheus_client import Gauge
from psutil import virtual_memory
import os


def monitor_host_metrics():
    # cpu
    process_cpu_usage_percents = Gauge('process_cpu_usage_percents', 'CPU Usage in percents')
    process_cpu_usage_percents.set_function(lambda: psutil.cpu_percent())
    process_cpu_time_user_mode = Gauge('process_cpu_time_user_mode', '')
    process_cpu_time_user_mode.set_function(lambda: psutil.cpu_times().user)
    process_cpu_time_system_mode = Gauge('process_cpu_time_system_mode', '')
    process_cpu_time_system_mode.set_function(lambda: psutil.cpu_times().system)
    process_cpu_time_idle_mode = Gauge('process_cpu_time_idle_mode', '')
    process_cpu_time_idle_mode.set_function(lambda: psutil.cpu_times().idle)
    # mem
    MEMORY_TOTAL = Gauge('host_memory_total_bytes', '')

    if ("MEMORY_LIMIT" in os.environ):
        mem_limit_str = os.environ["MEMORY_LIMIT"]
        MEMORY_TOTAL.set(mem_limit_str[:len(mem_limit_str) - 1])
    else:
        MEMORY_TOTAL.set_function(lambda: virtual_memory().total)

    MEMORY_CACHED = Gauge('host_memory_cached_bytes', '')
    MEMORY_CACHED.set_function(lambda: virtual_memory().cached)
    MEMORY_INACTIVE = Gauge('host_memory_inactive_bytes', '')
    MEMORY_INACTIVE.set_function(lambda: virtual_memory().inactive)
    MEMORY_ACTIVE = Gauge('host_memory_active_bytes', '')
    MEMORY_ACTIVE.set_function(lambda: virtual_memory().active)
    MEMORY_BUFFERS = Gauge('host_memory_buffers_bytes', '')
    MEMORY_BUFFERS.set_function(lambda: virtual_memory().buffers)
    MEMORY_FREE = Gauge('host_memory_free_bytes', '')
    MEMORY_FREE.set_function(lambda: virtual_memory().free)
    host_memory_used_bytes = Gauge('host_memory_used_bytes', '')
    host_memory_used_bytes.set_function(lambda: virtual_memory().used)
    MEMORY_PERCENT = Gauge('host_memory_percents', '')
    MEMORY_PERCENT.set_function(lambda: virtual_memory().percent)
    SWAP_MEMORY_PERCENT = Gauge('host_swap_memory_percent', '')
    SWAP_MEMORY_PERCENT.set_function(lambda: psutil.swap_memory().percent)
    SWAP_MEMORY_USED = Gauge('host_swap_memory_used_bytes', '')
    SWAP_MEMORY_USED.set_function(lambda: psutil.swap_memory().used)
    SWAP_MEMORY_FREE = Gauge('host_swap_memory_free_bytes', '')
    SWAP_MEMORY_FREE.set_function(lambda: psutil.swap_memory().free)

    # network
    network_bytes_sent_int = Gauge('network_bytes_sent_int', '', ["interface"])
    network_bytes_recv_int = Gauge('network_bytes_recv_int', 'Total bytes received via current interface',
                                   ["interface"])

    for interface in netifaces.interfaces():
        network_bytes_sent_int.labels(interface).set_function(lambda: net_stat.rx_tx_bytes(interface)[0])
        network_bytes_recv_int.labels(interface).set_function(lambda: net_stat.rx_tx_bytes(interface)[1])

    # //per second can be calculate from total

    network_bytes_sent = Gauge('host_net_tx_bytes', '')
    network_bytes_sent.set_function(lambda: psutil.net_io_counters().bytes_sent)

    network_bytes_recv = Gauge('network_bytes_recv', 'Total bytes received')
    network_bytes_recv.set_function(lambda: psutil.net_io_counters().bytes_recv)

    network_packets_sent = Gauge('network_packets_sent', '')
    network_packets_sent.set_function(lambda: psutil.net_io_counters().packets_sent)

    network_packets_recv = Gauge('network_packets_recv', '')
    network_packets_recv.set_function(lambda: psutil.net_io_counters().packets_recv)

    network_errin = Gauge('network_errin', '')
    network_errin.set_function(lambda: psutil.net_io_counters().errin)

    network_errout = Gauge('network_errout', '')
    network_errout.set_function(lambda: psutil.net_io_counters().errout)

    network_dropin = Gauge('network_dropin', '')
    network_dropin.set_function(lambda: psutil.net_io_counters().dropin)

    network_dropout = Gauge('network_dropout', '')
    network_dropout.set_function(lambda: psutil.net_io_counters().dropout)

    # disk IO
    DISK_READ = Gauge('host_disk_reads', 'Total reads for all disks')
    DISK_READ.set_function(lambda: disk_stat.disk_reads_persec())

    DISK_WRITE = Gauge('host_disk_writes', 'Total writes for all disks')
    DISK_WRITE.set_function(lambda: disk_stat.disk_writes_persec())

    host_disk_total = Gauge('host_disk_total', '')
    host_disk_total.set_function(lambda: psutil.disk_usage("/").total)
    host_disk_free = Gauge('host_disk_free', '')
    host_disk_free.set_function(lambda: psutil.disk_usage("/").free)
    host_disk_used = Gauge('host_disk_used', '')
    host_disk_used.set_function(lambda: psutil.disk_usage("/").used)
    host_disk_percent = Gauge('host_disk_percent', '')
    host_disk_percent.set_function(lambda: psutil.disk_usage("/").percent)

    # process_python_no_of_workers = Gauge('process_python_no_of_workers', '')
    # process_python_no_of_workers.set_function(lambda: multiprocessing.Pool()._processes)
