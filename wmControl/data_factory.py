from __future__ import annotations

from typing import Type

from wmControl.wlmConst import DataPackage, MeasureMode
from wmControl.wlmConst import Wavelength1, Wavelength2, Wavelength3, Wavelength4, Wavelength5, Wavelength6, Wavelength7, Wavelength8
from wmControl.wlmConst import Temperature, Distance, Linewidth, AnalogIn, AnalogOut
from wmControl.wlmConst import PID_P, PID_I, PID_D, PID_T, PID_dt
from wmControl.wlmConst import ExternalInput, DevitationSensitivityFactor


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
        self.__registered_data_types[package.mode] = package

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
data_factory.register(Wavelength2)
data_factory.register(Wavelength3)
data_factory.register(Wavelength4)
data_factory.register(Wavelength5)
data_factory.register(Wavelength6)
data_factory.register(Wavelength7)
data_factory.register(Wavelength8)
data_factory.register(Temperature)
data_factory.register(Distance)
data_factory.register(Linewidth)
data_factory.register(AnalogIn)
data_factory.register(AnalogOut)
data_factory.register(PID_P)
data_factory.register(PID_I)
data_factory.register(PID_D)
data_factory.register(PID_T)
data_factory.register(PID_dt)
data_factory.register(ExternalInput)
data_factory.register(DevitationSensitivityFactor)

#print(data_factory._DataTypeFactory__registered_data_types)
