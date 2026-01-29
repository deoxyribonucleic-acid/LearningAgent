from abc import ABC, abstractmethod


class LLMBase(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name


    @abstractmethod
    def inference(self, prompt: str) -> str:
        """Generate a response from the model based on the given prompt."""
        pass