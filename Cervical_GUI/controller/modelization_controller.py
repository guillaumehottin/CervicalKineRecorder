from PyQt5.QtCore import QObject


class ModelizationController(QObject):
    """
        This class is used to handle every action done on the acquisition view
        Here you can find button handler and attributes used to perform acquisition process
    """

    def __init__(self, view):
        """
        Function used to create the controller and init each attribute
        :param view: the corresponding view (here acquisition.py)
        """
        super(ModelizationController, self).__init__()

        # ATTRIBUTES
        self.view = view

