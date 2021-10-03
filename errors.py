"""
Module designed to contain any custom error handling classes.

Classes
-------
Error:
    base class that inherits the build in Exception class and is inherited in
    all custom error classes.
InputTooSmallError:
    error class that is raised if a value for an input is found to be below
    the low bound threshold for that input.
"""

class Error(Exception):
    """
    Base class for error handling.
    """

class InputTooSmallError(Error):
    """
    Error class used for when values are found below their minimum bounds.
    """
    def __init__(self, val, bound, var):
        """
        Constructor

        Parameters
        ----------
        val : int
            value found below minimum bound.
        bound : int
            minimum bound.
        var : str
            name of input variable found below bound.

        Returns
        -------
        None.

        """
        self.message = f"Param {var} is lower than the min value ({val} < {bound})."
        super().__init__(self.message)
