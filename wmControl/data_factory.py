from __future__ import annotations

from typing import Type

from wmControl.wlmConst import DataPackage, MeasureMode
#330
# DblVal imports
from wmControl.wlmConst import Wavelength1, Wavelength2, Wavelength3, Wavelength4, Wavelength5, Wavelength6, Wavelength7, Wavelength8
from wmControl.wlmConst import Temperature, Distance, Linewidth, AnalogIn, AnalogOut
from wmControl.wlmConst import PID_P, PID_I, PID_D, PID_T, PID_dt
from wmControl.wlmConst import ExternalInput, DevitationSensitivityFactor
# IntVal imports
from wmControl.wlmConst import FastMode, WideMode, ResultMode, ExposureMode, PulseMode, DisplayMode, AnalysisMode, SwitcherMode
from wmControl.wlmConst import Reduced, Range, Link, Operation, SwitcherChannel, PIDCourse, DeviationSensitivityDim
from wmControl.wlmConst import Min1, Min11, Min12, Min13, Min14, Min15, Min16, Min17, Min18, Min19
from wmControl.wlmConst import Max1, Max11, Max12, Max13, Max14, Max15, Max16, Max17, Max18, Max19
from wmControl.wlmConst import Avg1, Avg11, Avg12, Avg13, Avg14, Avg15, Avg16, Avg17, Avg18, Avg19
from wmControl.wlmConst import Min2, Min21, Min22, Min23, Min24, Min25, Min26, Min27, Min28, Min29
from wmControl.wlmConst import Max2, Max21, Max22, Max23, Max24, Max25, Max26, Max27, Max28, Max29
from wmControl.wlmConst import Avg2, Avg21, Avg22, Avg23, Avg24, Avg25, Avg26, Avg27, Avg28, Avg29
from wmControl.wlmConst import Exposure1, Exposure11, Exposure12, Exposure13, Exposure14, Exposure15, Exposure16, Exposure17, Exposure18
from wmControl.wlmConst import Exposure2, Exposure21, Exposure22, Exposure23, Exposure24, Exposure25, Exposure26, Exposure27, Exposure28


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

#print(data_factory._DataTypeFactory__registered_data_types)
