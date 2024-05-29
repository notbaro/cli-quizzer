from pathlib import Path
from quiz import Quiz
import pickle
from rich import print


def add_quiz(quiz: Quiz, path: Path = Path("quizzes.pkl")):
    try:
        with open(path, 'rb') as f:
            loaded_quizzes = pickle.load(f)
    except (EOFError, FileNotFoundError):
        loaded_quizzes = []

    loaded_quizzes.append(quiz)

    with open(path, 'wb') as f:
        pickle.dump(loaded_quizzes, f)


def bar(path: Path = Path("quizzes.pkl")):
    # Load the list from a file
    with open('quizzes.pkl', 'rb') as f:
        loaded_quizzes = pickle.load(f)
        for q in loaded_quizzes:
            print(q)

# Now loaded_quizzes is a list of Quiz objects