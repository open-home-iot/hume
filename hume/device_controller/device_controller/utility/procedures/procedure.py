from abc import abstractmethod


class Procedure:

    @abstractmethod
    def start_procedure(self, *args):
        """
        Called upon it being the caller's turn to execute.

        :param args: whatever arguments were given when queueing the procedure
        """
        ...
