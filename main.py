from pathlib import Path
import pickle
import random
from typing import Optional
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich.table import Table
from rich import print

from quiz import Quiz
from quiz_pickling import add_quiz

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def add(question: str, answers: Annotated[Optional[list[str]], typer.Argument()]) -> None:
    print(f"[magenta]Question: [/magenta][cyan]{question}[/cyan]")
    if answers is None:
        print("[bold red]Answers cannot be empty[/bold red]")
        raise typer.Exit()

    table = Table("#", "answer")
    for idx, ans in enumerate(answers, start=1):
        table.add_row(str(idx), f"[italic green]{ans}[/italic green]")
    console.print(table)

    key = -1
    while key < 0 or key >= len(answers):
        key = int(typer.prompt("Enter the # for the correct answers", type=int)) - 1

        if key < 0 or key >= len(answers):
            print("[bold red]Invalid key[/bold red]")

    path = Path(
        typer.prompt(
            "Enter the path to the quiz file (leave blank to use default)",
            default="quizzes.pkl",
        )
    )
    if path.is_file() and path.suffix in [".pkl", ".pickle"]:
        add_quiz(Quiz(question, answers, key), path)
        print(f"[bold green]Successfully saved at {path}[/bold green]✅")
    elif path.is_dir():
        add_quiz(Quiz(question, answers, key), path / "quizzes.pkl")
    else:
        print("[bold red]Invalid file/directory[/bold red]")
        raise typer.Exit()


def read_file(path: Path) -> list[Quiz]:
    if path.exists() and path.is_file() and path.suffix in [".pkl", ".pickle"]:
        with open(path, "rb") as f:
            quizzes: list[Quiz] = pickle.load(f)
            return quizzes
    else:
        print("[bold red]invalid file[/bold red]")
        raise typer.Exit()


@app.command()
def show(path: Annotated[Path, typer.Argument()]) -> None:
    quizzes: list[Quiz] = read_file(path)
    for idx, q in enumerate(quizzes, start=1):
        print(f"[magenta]Question [bold red]#{idx}[/]: [/][cyan]{q.question}[/]")

        table = Table(
            "#",
            "answer",
        )
        for idxx, ans in enumerate(q.answers, start=1):
            if idxx - 1 == q.key:
                table.add_row(
                    str(idxx),
                    f"[italic green]{ans}[/]✅",
                )
            else:
                table.add_row(str(idxx), f"[italic red]{ans}[/]")
        console.print(table)


@app.command()
def remove(path: Annotated[Path, typer.Argument()] = Path("quizzes.pkl")) -> None:
    quizzes = read_file(path)
    show(path)
    key = -1
    while key < 0 or key >= len(quizzes):
        key = int(typer.prompt("Enter the question # for deletion", type=int)) - 1

        if key < 0 or key >= len(quizzes):
            print("[bold red]Invalid #[/bold red]")
    quizzes.pop(key)
    with open(path, "wb") as f:
        pickle.dump(quizzes, f)
    print(f"[green]Sucessfully deleted question [red]#{key + 1}[/].[/]")


@app.command()
def quiz(path: Annotated[Path, typer.Argument()] = Path("quizzes.pkl")) -> None:
    quizzes = read_file(path)
    random.shuffle(quizzes)
    print(f"[yellow]There are {len(quizzes)} questions.")
    score = 0
    for idx, q in enumerate(quizzes, start=1):
        print(f"[magenta]Question [bold red]#{idx}[/]: [/][cyan]{q.question}[/]")
        table = Table(
            "#",
            "answer",
        )
        for idxx, ans in enumerate(q.answers, start=1):
            table.add_row(
                str(idxx),
                f"{ans}",
            )
        console.print(table)

        key = -1
        while key < 0 or key >= len(q.answers):
            key = int(typer.prompt("Enter the # for the correct answers", type=int)) - 1
            if key < 0 or key >= len(q.answers):
                print("[bold red]Invalid key[/bold red]")

        if key == q.key:
            score += 1
            print("🎉[italic green]Congratz! That is the correct answer🎉")
        else:
            print(
                f"❌[red]Oops. That's incorrect. The right answer was [italic green]#{q.key + 1}[/].[/]❌"
            )
        print(f"[yellow]Your current score is {score}/{idx}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
