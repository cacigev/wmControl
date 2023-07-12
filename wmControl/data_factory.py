from __future__ import annotations

from typing import Type

from wmControl.wlmConst import DataPackage, MeasureMode, Wavelength1


class DataTypeFactory:
    """
    The factory. Do not import this, as it is instantiated below to create a
    class object.
    """

    def __init__(self):
        self.__registered_data_types: dict[MeasureMode, Type[DataPackage]] = {}

    def register(self, package: Type[DataPackage]):
        """
        Register a new type of data package with the factory
        """
        self.__registered_data_types[package.MODE] = package

    def get(self, mode: MeasureMode | int, *args, **kwargs) -> DataPackage:
        """
        Create a new instance of the data class from the mode integer and the parameters passed
        """
        try:
            return self.__registered_data_types[mode](*args, **kwargs)
        except KeyError:
            raise ValueError(f"Unknown data package received: {mode}") from None


data_factory = DataTypeFactory()

data_factory.register(Wavelength1)
