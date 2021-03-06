import cid as py_cid
from typing import Union


class Block:
    """
    Represents an immutable block of data that is uniquely referenced with a cid.
    """

    def __init__(self, data, cid: Union[py_cid.CIDv0, py_cid.CIDv1]):
        """
        Represents an immutable block of data that is uniquely referenced with a cid.

        :param data: An object supporting the

        :param cid: A cid
        """
        try:
            memoryview(data)
        except TypeError:
            raise ValueError("Data must be an object supporting the buffer protocol.")
        if not py_cid.is_cid(str(cid)):
            raise ValueError(f"{cid} is not a valid cid")
        self._data = data
        self._cid = cid

    @property
    def data(self):
        """
        The data of this block

        :return: The data of this block
        """
        return self._data

    @data.setter
    def data(self, val):
        raise AttributeError("Cannot change the data of a block")

    @property
    def cid(self) -> Union[py_cid.CIDv0, py_cid.CIDv1]:
        """
        The cid of this block

        :return: The cid of this block
        """
        return self._cid

    @cid.setter
    def cid(self, val: Union[py_cid.CIDv0, py_cid.CIDv1]):
        raise AttributeError("Cannot change the cid of a block")
