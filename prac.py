import os
import platform
import psutil
import shutil
import socket
import subprocess
import time
from rich.console import Console
from datetime import timedelta
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box  
from rich.box import ROUNDED
from subprocess import run, PIPE

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def fetch_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    uptime = timedelta(seconds=uptime_seconds)
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

def fetch_cpu_info():
    cpu = "Unknown CPU"
    try:
        if shutil.which("lscpu"):
            cpu_info = run(["lscpu"], stdout=PIPE, text=True).stdout
            cpu = next((line.split(":")[1].strip() for line in cpu_info.splitlines() if "Model name" in line), "Unknown CPU")
        else:
            cpu = platform.processor()
    except Exception:
        pass
    return cpu or "Unknown CPU"

def fetch_gpu_info():
    gpu = "Unknown GPU"
    try:
        if shutil.which("lspci"):
            lspci_output = run(["lspci"], stdout=PIPE, text=True).stdout
            gpu = next(
                (line for line in lspci_output.splitlines() if "VGA compatible controller" in line or "3D controller" in line),
                "Unknown GPU"
            )
    except Exception:
        pass
    return gpu.split(":")[-1].strip() if gpu != "Unknown GPU" else gpu

def fetch_theme():
    theme = "Unknown Theme"
    try:
        if os.environ.get("GTK_THEME"):
            theme = os.environ["GTK_THEME"]
        elif shutil.which("gsettings"):
            theme = run(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"], stdout=PIPE, text=True).stdout.strip().strip("'")
    except Exception:
        pass
    return theme

def fetch_default_browser():
    browser = "Unknown Browser"
    try:
        if shutil.which("xdg-settings"):
            browser = run(["xdg-settings", "get", "default-web-browser"], stdout=PIPE, text=True).stdout.strip()
    except Exception:
        pass
    return browser

def fetch_system_info():
    os_name = platform.system()
    kernel = platform.release()
    hostname = socket.gethostname()
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    uptime = fetch_uptime()
    shell = os.environ.get("SHELL", "Unknown Shell")
    theme = fetch_theme()
    browser = fetch_default_browser()

    return {
        "OS": os_name,
        "Kernel": kernel,
        "CPU": fetch_cpu_info(),
        "GPU": fetch_gpu_info(),
        "RAM": f"{ram} GB",
        "Hostname": hostname,
        "Shell": shell,
        "Uptime": uptime,
        "Theme": theme,
        "Browser": browser,
    }

def display_menu():
    console.print(Panel("[bold magenta]Welcome to the Enhanced Linux TUI[/bold magenta]", width=60, expand=False))
    table = Table(title="Main Menu", show_header=True, header_style="bold cyan", box=ROUNDED)
    table.add_column("Option", justify="center", style="bold white")
    table.add_column("Description", justify="left", style="bold yellow")
    
    options = [
        ("1", "View System Information"),
        ("2", "Disk Usage"),
        ("3", "Network Information"),
        ("4", "Processes Information"),
        ("5", "Temperature Monitoring"),
        ("6", "Manage Packages"),
        ("7", "System Updates"),
        ("8", "User Management"),
        ("9", "Run Custom Command"),
        ("10", "Filter Processes"),
        ("11", "Exit"),
    ]
    for opt, desc in options:
        table.add_row(opt, desc)
    console.print(table)
    console.print(Panel("Shortcuts: [bold cyan]Ctrl+C[/bold cyan] to quit | [bold cyan]Enter[/bold cyan] to select", box=ROUNDED))

def system_info():
    console.print("[bold green]System Information[/bold green]")
    sys_info = fetch_system_info()

    info_table = Table(show_header=False, box=ROUNDED)
    info_table.add_column("Property", style="bold cyan", justify="right")
    info_table.add_column("Value", style="bold yellow")

    for key, value in sys_info.items():
        info_table.add_row(key, value)

    console.print(info_table)

def disk_usage():
    console.print("[bold green]Disk Usage[/bold green]")
    disk = psutil.disk_usage("/")
    total = round(disk.total / (1024 ** 3), 2)
    used = round(disk.used / (1024 ** 3), 2)
    free = round(disk.free / (1024 ** 3), 2)
    percent = disk.percent

    table = Table(show_header=True, header_style="bold blue", box=ROUNDED)
    table.add_column("Total", justify="center")
    table.add_column("Used", justify="center")
    table.add_column("Free", justify="center")
    table.add_column("Usage", justify="center")

    table.add_row(f"{total} GB", f"{used} GB", f"{free} GB", f"{percent}%")
    console.print(table)

def network_info():
    console.print("[bold green]Network Information[/bold green]")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    table = Table(show_header=True, header_style="bold blue", box=ROUNDED)
    table.add_column("Hostname", justify="center")
    table.add_column("IP Address", justify="center")

    table.add_row(hostname, ip_address)
    console.print(table)

def processes_info():
    console.print("[bold green]Processes Information[/bold green]")
    processes = [(p.info["pid"], p.info["name"], p.info["memory_percent"]) for p in psutil.process_iter(['pid', 'name', 'memory_percent'])]
    processes.sort(key=lambda x: x[2], reverse=True)
    
    table = Table(title="Top Processes by Memory Usage", show_header=True, header_style="bold blue", box=ROUNDED)
    table.add_column("PID", justify="center")
    table.add_column("Name", justify="left")
    table.add_column("Memory Usage (%)", justify="center")

    for pid, name, mem_usage in processes[:10]:
        table.add_row(str(pid), name, f"{mem_usage:.2f}%")
    console.print(table)

def temperature_monitoring():
    console.print("[bold green]Temperature Monitoring[/bold green]")
    sensors = psutil.sensors_temperatures()
    if not sensors:
        console.print("[bold red]No temperature sensors found.[/bold red]")
        return
    for sensor, temp_list in sensors.items():
        for temp in temp_list:
            if temp.label:
                console.print(f"{temp.label}: {temp.current}°C")
            else:
                console.print(f"{sensor}: {temp.current}°C")

def detect_package_manager():
    """Detect the system's package manager."""
    if shutil.which("pacman"):
        return "pacman"
    elif shutil.which("apt"):
        return "apt"
    elif shutil.which("dnf"):
        return "dnf"
    elif shutil.which("yum"):
        return "yum"
    else:
        return None

def list_installed_packages(package_manager):
    match package_manager:
        case "apt":
            os.system("dpkg-query -l")
        case "pacman":
            os.system("pacman -Q")
        case "dnf" | "yum":
            os.system(f"{package_manager} list installed")

def install_package(package_manager, package):
    try:
        if package_manager == "pacman":
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", package], check=True)
        elif package_manager == "apt":
            subprocess.run(["sudo", "apt-get", "install", "-y", package], check=True)
        elif package_manager == "dnf":
            subprocess.run(["sudo", "dnf", "install", "-y", package], check=True)
        else:
            console.print("[bold red]Unsupported package manager.[/bold red]")
            return
        console.print(f"[bold green]Successfully installed {package} using {package_manager}.[/bold green]")
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Failed to install {package} using {package_manager}.[/bold red]")

def remove_package(package_manager, package):
    """Remove a package based on the package manager."""
    match package_manager:
        case "apt":
            os.system(f"sudo apt remove -y {package}")
        case "pacman":
            os.system(f"sudo pacman -Rns --noconfirm {package}")
        case "dnf" | "yum":
            os.system(f"sudo {package_manager} remove -y {package}")

def update_system(package_manager):
    """Update the system based on the package manager."""
    match package_manager:
        case "apt":
            os.system("sudo apt update && sudo apt upgrade -y")
        case "pacman":
            os.system("sudo pacman -Syu --noconfirm")
        case "dnf" | "yum":
            os.system(f"sudo {package_manager} update -y && sudo {package_manager} upgrade -y")

from rich import box  

def manage_packages():
    package_manager = detect_package_manager()
    if not package_manager:
        console.print("[bold red]No supported package manager detected.[/bold red]")
        return
    
    console.print(Panel(f"[bold cyan]{package_manager.upper()} Package Management[/bold cyan]"))
    table = Table(box=box.ROUNDED)  
    table.add_column("Option", justify="center", style="bold white")
    table.add_column("Description", justify="left", style="bold yellow")
    options = [
        ("1", "List Installed Packages"),
        ("2", "Install a Package"),
        ("3", "Remove a Package"),
        ("4", "Update System"),
        ("5", "Return to Main Menu"),
    ]
    for opt, desc in options:
        table.add_row(opt, desc)
    console.print(table)
    
    choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="5")
    
    match choice:
        case "1":  
            list_installed_packages(package_manager)
        case "2":  
            package = Prompt.ask("[bold cyan]Enter package name to install[/bold cyan]")
            install_package(package_manager, package)
        case "3":  
            package = Prompt.ask("[bold red]Enter package name to remove[/bold red]")
            remove_package(package_manager, package)
        case "4":  
            update_system(package_manager)
        case "5":  
            return

def user_management():
    console.print(Panel("[bold cyan]User Management[/bold cyan]"))
    choice = Prompt.ask("Do you want to [bold green](a)dd[/bold green] or [bold red](r)emove[/bold red] a user?", choices=["a", "r"], default="a")
    
    if choice == "a":
        username = Prompt.ask("[bold cyan]Enter username to add[/bold cyan]")
        result = os.system(f"sudo useradd -m {username} && sudo passwd {username}")
        if result != 0:
            console.print("[bold red]Failed to add user. Ensure you have proper permissions.[/bold red]")
    elif choice == "r":
        username = Prompt.ask("[bold red]Enter username to remove[/bold red]")
        result = os.system(f"sudo userdel -r {username}")
        if result != 0:
            console.print("[bold red]Failed to remove user. Ensure you have proper permissions.[/bold red]")

def run_custom_command():
    command = Prompt.ask("[bold yellow]Enter a custom command to execute[/bold yellow]")
    os.system(command)

def filter_processes():
    keyword = Prompt.ask("[bold cyan]Enter a keyword to filter processes[/bold cyan]")
    processes = [p.info for p in psutil.process_iter(['pid', 'name']) if keyword.lower() in p.info['name'].lower()]
    
    if processes:
        table = Table(title="Filtered Processes", show_header=True, header_style="bold blue", box=ROUNDED)
        table.add_column("PID", justify="center")
        table.add_column("Name", justify="left")
        for p in processes:
            table.add_row(str(p['pid']), p['name'])
        console.print(table)
    else:
        console.print("[bold red]No matching processes found.[/bold red]")

def main():
    while True:
        clear_screen()
        display_menu()
        choice = Prompt.ask("Enter your choice", choices=[str(i) for i in range(1, 12)], default="11")
        clear_screen()
        match choice:
            case "1":
                system_info()
            case "2":
                disk_usage()
            case "3":
                network_info()
            case "4":
                processes_info()
            case "5":
                temperature_monitoring()
            case "6":
                manage_packages()
            case "7":
                system_info()
            case "8":
                user_management()
            case "9":
                run_custom_command()
            case "10":
                filter_processes()
            case "11":
                console.print("[bold red]Exiting...[/bold red]")
                break
        console.input("[bold yellow]Press Enter to return to the menu...[/bold yellow]")

if __name__ == "__main__":
    main()

