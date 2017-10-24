

def mem_stats():
    with open('/proc/meminfo') as f:
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1]) * 1024
            elif line.startswith('Active: '):
                mem_active = int(line.split()[1]) * 1024
            elif line.startswith('MemFree:'):
                mem_free = (int(line.split()[1]) * 1024)
            elif line.startswith('Cached:'):
                mem_cached = (int(line.split()[1]) * 1024)
            elif line.startswith('SwapTotal: '):
                swap_total = (int(line.split()[1]) * 1024)
            elif line.startswith('SwapFree: '):
                swap_free = (int(line.split()[1]) * 1024)
    return (mem_active, mem_total, mem_cached, mem_free, swap_total, swap_free)
