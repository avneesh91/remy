from abc import ABCMeta, abstractmethod

class BaseHandler(metaclass=ABCMeta):

    @abstractmethod
    def run_input_prompt(self):
        pass

    @abstractmethod
    def run(self):
        pass


