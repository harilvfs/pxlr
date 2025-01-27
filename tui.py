from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from datetime import datetime
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output.defaults import create_output
import asyncio

console = Console()
layout = Layout()

tabs = ["Welcome", "Workspace 1", "Workspace 2", "Workspace 3"]
selected_tab = 0 
modes = {"normal": "[bold cyan]NORMAL[/bold cyan]", "insert": "[bold green]INSERT[/bold green]"}
current_mode = "normal"


def render_header():
    return Panel(
        Text("📜 Aayush's Neovim TUI Clone", justify="center"),
        style="bold blue",
        title=f"Mode: {modes[current_mode]}",
        title_align="left",
    )


def render_sidebar():
    sidebar = ""
    for i, tab in enumerate(tabs):
        if i == selected_tab:
            sidebar += f"[bold green]> {tab}[/bold green]\n"
        else:
            sidebar += f"  {tab}\n"
    return Panel(
        sidebar,
        title="[bold blue]Navigation[/bold blue]",
        border_style="cyan",
        width=30,
    )


def render_main_content():
    content_map = {
        "Welcome": "Welcome to your Neovim-inspired TUI!",
        "Workspace 1": "Manage your first workspace here.",
        "Workspace 2": "Organize tasks for Workspace 2.",
        "Workspace 3": "Configure Workspace 3 settings.",
    }
    content = content_map.get(tabs[selected_tab], "Unknown Workspace")
    return Panel(
        Text(content, justify="center"),
        title=f"[bold green] {tabs[selected_tab]} [/bold green]",
        border_style="bright_white",
    )


def render_footer():
    current_time = datetime.now().strftime("%H:%M:%S")
    return Panel(
        f"  {current_time} | Press ':q' to quit | Use 'hjkl' to navigate | Mode: {modes[current_mode]}",
        style="bold blue",
    )


def update_layout():
    layout["header"].update(render_header())
    layout["sidebar"].update(render_sidebar())
    layout["content"].update(render_main_content())
    layout["footer"].update(render_footer())

key_bindings = KeyBindings()

@key_bindings.add("j")
def move_down(event):
    global selected_tab
    if current_mode == "normal":
        selected_tab = (selected_tab + 1) % len(tabs)
        update_layout()


@key_bindings.add("k")
def move_up(event):
    global selected_tab
    if current_mode == "normal":
        selected_tab = (selected_tab - 1) % len(tabs)
        update_layout()


@key_bindings.add("i")
def switch_to_insert_mode(event):
    global current_mode
    current_mode = "insert"
    update_layout()


@key_bindings.add("escape")
def switch_to_normal_mode(event):
    global current_mode
    current_mode = "normal"
    update_layout()


@key_bindings.add(":")
def quit_tui(event):
    event.app.exit()

async def run_tui():
    """Run the Neovim-inspired TUI with rich and prompt_toolkit."""
    global layout

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="content", ratio=1),
    )

    app = Application(
        layout=None,
        full_screen=True,
        key_bindings=key_bindings,
        mouse_support=False,
    )

    with Live(layout, console=console, refresh_per_second=10, screen=True):
        update_layout()
        await app.run_async()


if __name__ == "__main__":
    try:
        asyncio.run(run_tui())
    except KeyboardInterrupt:
        console.print("[bold green]Exiting... Goodbye![/bold green]")

