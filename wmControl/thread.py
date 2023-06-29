import logging

from wmControl import control, wlmConst, wlmData


class Callback:
    version = 0
    put = None

    # Prints all measured frequencies of one WM
    # Unit: THz
    def frequencysProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int):
        const_to_channel = {
            wlmConst.MeasureMode.cmiWavelength1: 1,
            wlmConst.MeasureMode.cmiWavelength2: 2,
            wlmConst.MeasureMode.cmiWavelength3: 3,
            wlmConst.MeasureMode.cmiWavelength4: 4,
            wlmConst.MeasureMode.cmiWavelength5: 5,
            wlmConst.MeasureMode.cmiWavelength6: 6,
            wlmConst.MeasureMode.cmiWavelength7: 7,
            wlmConst.MeasureMode.cmiWavelength8: 8,
        }

        try:
            mode = wlmConst.MeasureMode(mode)
        except ValueError:
            self.__logger.warning(
                "Unknown status received: '%s' is not defined. Parameters: %s, %s, %s, %s, %s",
                mode,
                ver,
                mode,
                int_val,
                double_val,
                result,
            )
        else:
            if (ver == self.version) and (mode in const_to_channel):
                self.__logger.info(
                    "Time: %s, WM: %s, Channel: %s, Frequency: %.8f",
                    int_val,
                    ver,
                    const_to_channel[mode],
                    299792.458 / double_val,
                )

    # Prints all measured wavelengths one WM
    # Unit: nm
    def wavelengthsProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int):
        const_to_channel = {
            wlmConst.MeasureMode.cmiWavelength1: 1,
            wlmConst.MeasureMode.cmiWavelength2: 2,
            wlmConst.MeasureMode.cmiWavelength3: 3,
            wlmConst.MeasureMode.cmiWavelength4: 4,
            wlmConst.MeasureMode.cmiWavelength5: 5,
            wlmConst.MeasureMode.cmiWavelength6: 6,
            wlmConst.MeasureMode.cmiWavelength7: 7,
            wlmConst.MeasureMode.cmiWavelength8: 8,
        }

        if (ver == self.version) and (mode in const_to_channel):
            print(f"Time:{int_val}, WM:{ver}, Channel:{const_to_channel[mode]}, Wavelength:{double_val:.8f}")

    # Prints all measured wavelengths of all WMs connected to the control-PC
    # Unit: nm
    def allwavelengthsProcEx(self, Ver, Mode, IntVal, DblVal, Res1):
        if Mode == wlmConst.MeasureMode.cmiWavelength1:
            # print("Time:{}, WM:{}, Channel:1, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength2:
            # print("Time:{}, WM:{}, Channel:2, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength3:
            # print("Time:{}, WM:{}, Channel:3, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength4:
            # print("Time:{}, WM:{}, Channel:4, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength5:
            # print("Time:{}, WM:{}, Channel:5, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength6:
            # print("Time:{}, WM:{}, Channel:6, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength7:
            # print("Time:{}, WM:{}, Channel:7, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.MeasureMode.cmiWavelength8:
            # print("Time:{}, WM:{}, Channel:8, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])

    def getSwitchedChannel(self, Ver, Mode, IntVal, DblVal, Res1):
        if Ver == self.version and Mode == wlmConst.MeasureMode.cmiSwitcherChannel:
            print(
                f"Time:{Res1}, WM:{Ver}, Active Channel: {IntVal}, Getter-state:{DblVal} Wavelength:{wlmData.dll.GetWavelengthNum(IntVal, 0):.8f}"
            )

    def __init__(self, ver, wavemeter):
        self.__logger = logging.getLogger(__name__)
        self.version = ver
        # self.put = wavemeter.putBfr
