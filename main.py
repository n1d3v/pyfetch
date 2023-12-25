import psutil
import platform
import GPUtil as GPU
import subprocess
import os

# OS Logos
tux_logo = '''    .--.
   |o_o |
   |:_/ |
  //   \\ \\
 (|     | )
/'\\_   _/`\\
\\___)=(___/'''

windows_logo = ''' ___   ___ 
|   | |   |
|___| |___|
 ___   ___ 
|   | |   |
|___| |___|'''

# Grab sysinfo
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
        try:
            process = subprocess.Popen(
                "wmic cpu get name", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            output, _ = process.communicate()
            output = output.decode("utf-8").strip().split("\n")
            return output[1] if len(output) > 1 else "CPU Name Not Found"
        except Exception as e:
            print(f"Error while fetching CPU name: {e}")
            return "CPU Name Not Found"
    elif platform.system() == 'Darwin':
        return platform.uname().processor
    elif platform.system() == 'Linux':
        with open('/proc/cpuinfo') as f:
            for line in f:
                if line.strip() and line.rstrip('\n').startswith('model name'):
                    return line.rstrip('\n').split(':')[1].strip()
    return 'CPU Name Not Found'

def get_shell():
    if platform.system() == 'Windows':
        return "CMD / PS"
    else:
        shell = os.environ.get('SHELL')
        if shell:
            return shell.split('/')[-1]
        return "Shell not detected"

def get_desktop_environment():
    if platform.system() == 'Windows':
        return "Windows Explorer"
    else:
        de = os.environ.get('XDG_CURRENT_DESKTOP')
        if de:
            return de
        wm = subprocess.getoutput('echo $XDG_SESSION_DESKTOP')
        if wm:
            return wm
        return "DE/WM not detected"

# Fetch the info collected
def fetch_sys_info():
    os_info = get_os_info()
    kernel_version = get_kernel_version()
    cpu_name = get_cpu_name()
    cpu_utilization = f"{psutil.cpu_percent()}% utilized"
    mem = psutil.virtual_memory()
    mem_used = f"{int(mem.used / (1024 * 1024))}MB / {int(mem.total / (1024 * 1024))}MB"
    gpus = GPU.getGPUs()
    gpu_info = [f"{gpu.name}" for gpu in gpus]
    shell_info = get_shell()
    desktop_env = get_desktop_environment()

    system_info = {
        'OS': os_info,
        'Kernel': kernel_version,
        'Shell': shell_info,
        'CPU': f"{cpu_name} - {cpu_utilization}",
        'Memory': mem_used,
        'GPU': ', '.join(gpu_info),
        'DE/WM': desktop_env
    }
    return system_info

# Shit the info out
def display_sys_info(system_info, logo):
    logo_lines = logo.split('\n')
    max_logo_length = max(len(line) for line in logo_lines)

    total_lines = max(len(logo_lines), len(system_info))

    for line_num in range(total_lines):
        logo_line = logo_lines[line_num] if line_num < len(logo_lines) else ''

        sys_info_line = list(system_info.items())[line_num] if line_num < len(system_info) else None

        if sys_info_line:
            key, value = sys_info_line
            if key == 'GPU':
                print(f"{logo_line}{' ' * (max_logo_length - len(logo_line))}    {key}: {value}")
            else:
                print(f"{logo_line}{' ' * (max_logo_length - len(logo_line))}    {key}: {value}")
        else:
            print(f"{logo_line}{' ' * (max_logo_length - len(logo_line))}")

if __name__ == "__main__":
    sys_info = fetch_sys_info()

    if platform.system() == 'Windows':
        display_sys_info(sys_info, windows_logo)
    else:
        display_sys_info(sys_info, tux_logo)
