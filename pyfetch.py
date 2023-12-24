import psutil
import platform
import GPUtil as GPU
import subprocess

def get_os_info():
    try:
        distribution = subprocess.check_output(['lsb_release', '-ds']).decode().strip()
        return distribution if distribution else platform.platform()
    except FileNotFoundError:
        return platform.platform()

def get_kernel_version():
    return platform.uname().release

def get_cpu_name():
    if platform.system() == 'Windows':
        return platform.processor()
    elif platform.system() == 'Darwin':
        return platform.uname().processor
    elif platform.system() == 'Linux':
        with open('/proc/cpuinfo') as f:
            for line in f:
                if line.strip() and line.rstrip('\n').startswith('model name'):
                    return line.rstrip('\n').split(':')[1].strip()
    return 'CPU Name Not Found'

def fetch_sys_info():
    # OS info
    os_info = get_os_info()

    # Kernel info
    kernel_version = get_kernel_version()

    # CPU info
    cpu_name = get_cpu_name()
    cpu_utilization = f"{psutil.cpu_percent()}% utilization"

    # Memory info
    mem = psutil.virtual_memory()
    mem_used = f"{int(mem.used / (1024 * 1024))}MB / {int(mem.total / (1024 * 1024))}MB"

    # Disk info
    disk_info = psutil.disk_partitions()
    disk_details = []
    for disk in disk_info:
        if 'rw' in disk.opts:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            disk_details.append(f"{disk.device} - {disk.mountpoint}: "
                                f"{disk_usage.used / (1024 * 1024 * 1024):.2f}GB used / "
                                f"{disk_usage.total / (1024 * 1024 * 1024):.2f}GB total")

    # GPU info
    gpus = GPU.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append(f"{gpu.name}: {gpu.memoryUsed}MB used / {gpu.memoryTotal}MB total")

    system_info = {
        'OS': os_info,
        'Kernel': kernel_version,
        'CPU': f"{cpu_name} - {cpu_utilization}",
        'Memory': mem_used,
        'Disks': disk_details,
        'GPU': ', '.join(gpu_info)
    }
    return system_info

def display_sys_info(system_info):
    for key, value in system_info.items():
        if key == 'Disks':
            print("Disks / Partitions:")
            if value:
                for disk in value:
                    print(f"  - {disk}")
            else:
                print("  - No additional disks / partitions found.")
        elif key == 'GPU':
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    sys_info = fetch_sys_info()
    display_sys_info(sys_info)
