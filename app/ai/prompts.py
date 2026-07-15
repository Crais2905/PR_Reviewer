from enum import Enum


class AIPrompts(Enum):
    DIFF_REVIEW = """
        I provide you a code difference in my git repo
        Your task: analys this difference and give me review
        If you find any problems -> add to response and describe it 
        
        Do not ask me any questions or add explanations.
        Do not write explanations, comments, or markdown
        
        My git difference: {diff}
    """

    def render(self, **kwargs):
        return self.value.format(**kwargs)
