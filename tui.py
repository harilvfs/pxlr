from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.tree import Tree
from rich.text import Text
from time import strftime

console = Console()

def render_header():
    return Panel(
        "📜 [bold white on blue] Aayush's Modern Script TUI [/bold white on blue]",
        height=3,
        style="on blue",
        title="Modern TUI",
    )

def render_sidebar(selected_tab):
    tree = Tree("🌲 [bold cyan]Workspaces[/bold cyan]")
    for workspace in ["Welcome", "Workspace 1", "Workspace 2", "Workspace 3"]:
        style = "yellow" if workspace != selected_tab else "green bold"
        tree.add(f"[{style}]{workspace}[/{style}]")
    return Panel(tree, title="[bold blue]Navigation[/bold blue]", border_style="cyan", width=30)

def render_main_content(selected_tab):
    content_map = {
        "Welcome": "Welcome to your modern TUI!\n\nSelect an option from the sidebar.",
        "Workspace 1": "Workspace 1 Content:\n\nManage your first workspace here.",
        "Workspace 2": "Workspace 2 Content:\n\nOrganize tasks and details for Workspace 2.",
        "Workspace 3": "Workspace 3 Content:\n\nConfigure and review settings for Workspace 3.",
    }
    content = content_map.get(selected_tab, "Unknown Workspace Selected!")
    return Panel(
        Text(content, justify="center"),
        title=f"[bold green] {selected_tab} [/bold green]",
        border_style="bright_white",
        expand=True,
    )

def render_footer():
    current_time = strftime("%H:%M:%S")
    footer_content = f"[bold] {current_time} | Type 'exit' to quit [/bold]"
    return Panel(
        footer_content,
        height=3,
        style="on blue",
    )

def main():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="content", ratio=1),
    )

    selected_tab = "Welcome"  

    while True:
        layout["header"].update(render_header())
        layout["sidebar"].update(render_sidebar(selected_tab))
        layout["content"].update(render_main_content(selected_tab))
        layout["footer"].update(render_footer())

        console.clear()
        console.print(layout)

        console.print(
            "[bold yellow]Navigate by entering: Welcome, Workspace 1, Workspace 2, Workspace 3[/bold yellow]"
            "\n[bold yellow]Or type 'exit' to quit.[/bold yellow]"
        )
        user_input = console.input("[bold cyan]> [/bold cyan]").strip()

        if user_input.lower() == "exit":
            console.print("[bold green]Exiting... Have a great day![/bold green]")
            break
        elif user_input in ["Welcome", "Workspace 1", "Workspace 2", "Workspace 3"]:
            selected_tab = user_input
        else:
            console.print("[bold red]Invalid input! Please try again.[/bold red]")

if __name__ == "__main__":
    main()

