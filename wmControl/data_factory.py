from __future__ import annotations

from typing import Type

from wmControl.wlmConst import *


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

# DblVal
data_factory.register(Wavelength1)
data_factory.register(Wavelength2)
data_factory.register(Wavelength3)
data_factory.register(Wavelength4)
data_factory.register(Wavelength5)
data_factory.register(Wavelength6)
data_factory.register(Wavelength7)
data_factory.register(Wavelength8)
data_factory.register(Temperature)
data_factory.register(Pressure)
data_factory.register(TimeTick)
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
data_factory.register(DeviationSensitivityFactor)
#
data_factory.register(FastMode)
data_factory.register(WideMode)
data_factory.register(ResultMode)
data_factory.register(ExposureMode)
data_factory.register(PulseMode)
data_factory.register(DisplayMode)
data_factory.register(AnalysisMode)
data_factory.register(SwitcherMode)
data_factory.register(Reduced)
data_factory.register(Range)
data_factory.register(Link)
data_factory.register(Operation)
data_factory.register(SwitcherChannel)
data_factory.register(PIDCourse)
data_factory.register(DeviationSensitivityDim)
#
data_factory.register(Min1)
data_factory.register(Min11)
data_factory.register(Min12)
data_factory.register(Min13)
data_factory.register(Min14)
data_factory.register(Min15)
data_factory.register(Min16)
data_factory.register(Min17)
data_factory.register(Min18)
data_factory.register(Min19)
data_factory.register(Min2)
data_factory.register(Min21)
data_factory.register(Min22)
data_factory.register(Min23)
data_factory.register(Min24)
data_factory.register(Min25)
data_factory.register(Min26)
data_factory.register(Min27)
data_factory.register(Min28)
data_factory.register(Min29)
data_factory.register(Max1)
data_factory.register(Max11)
data_factory.register(Max12)
data_factory.register(Max13)
data_factory.register(Max14)
data_factory.register(Max15)
data_factory.register(Max16)
data_factory.register(Max17)
data_factory.register(Max18)
data_factory.register(Max19)
data_factory.register(Max2)
data_factory.register(Max21)
data_factory.register(Max22)
data_factory.register(Max23)
data_factory.register(Max24)
data_factory.register(Max25)
data_factory.register(Max26)
data_factory.register(Max27)
data_factory.register(Max28)
data_factory.register(Max29)
data_factory.register(Avg1)
data_factory.register(Avg11)
data_factory.register(Avg12)
data_factory.register(Avg13)
data_factory.register(Avg14)
data_factory.register(Avg15)
data_factory.register(Avg16)
data_factory.register(Avg17)
data_factory.register(Avg18)
data_factory.register(Avg19)
data_factory.register(Avg2)
data_factory.register(Avg21)
data_factory.register(Avg22)
data_factory.register(Avg23)
data_factory.register(Avg24)
data_factory.register(Avg25)
data_factory.register(Avg26)
data_factory.register(Avg27)
data_factory.register(Avg28)
data_factory.register(Avg29)
data_factory.register(Exposure1)
data_factory.register(Exposure11)
data_factory.register(Exposure12)
data_factory.register(Exposure13)
data_factory.register(Exposure14)
data_factory.register(Exposure15)
data_factory.register(Exposure16)
data_factory.register(Exposure17)
data_factory.register(Exposure18)
data_factory.register(Exposure2)
data_factory.register(Exposure21)
data_factory.register(Exposure22)
data_factory.register(Exposure23)
data_factory.register(Exposure24)
data_factory.register(Exposure25)
data_factory.register(Exposure26)
data_factory.register(Exposure27)
data_factory.register(Exposure28)
data_factory.register(Power1)
data_factory.register(Power2)
data_factory.register(Power3)
data_factory.register(Power4)
data_factory.register(Power5)
data_factory.register(Power6)
data_factory.register(Power7)
data_factory.register(Power8)
data_factory.register(WavemeterServerShutdown)
data_factory.register(WavemeterServerStart)
data_factory.register(WavemeterServerInitialized)
