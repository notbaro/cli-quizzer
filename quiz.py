class Quiz:
    def __init__(self, question: str, answers: list[str], key: int):
        self.question = question
        self.answers = answers
        self.key = key
        
    def __repr__(self) -> str:
        return f'{self.question}, {self.answers}, {self.key}'
    
    