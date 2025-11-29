import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from src.graph import app

console = Console()

def main():
    load_dotenv()
    
    # Safety Check
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]CRITICAL ERROR:[/bold red] OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    query = "Analyze why ROAS dropped last week"
    
    initial_state = {
        "query": query,
        "retry_count": 0
    }

    console.print(Panel.fit(
        f"[bold cyan]Kasparro Agentic Analyst[/bold cyan]\n"
        f"[white]Query:[/white] {query}\n"
        f"[dim]Engine: OpenAI GPT-4 + LangGraph[/dim]",
        border_style="cyan"
    ))

    try:
        final_state = app.invoke(initial_state)
        
        console.print("\n[bold green]Analysis Workflow Complete![/bold green]")
        
        if final_state.get("hypothesis"):
            hypo = final_state["hypothesis"].get("hypothesis", "No hypothesis found")
            console.print(f"\n[bold yellow]Final Diagnosis:[/bold yellow] {hypo}")
        
        console.print(f"Full Report saved to: [underline]reports/final_report.json[/underline]")

    except Exception as e:
        console.print(f"\n[bold red]Workflow Failed:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()