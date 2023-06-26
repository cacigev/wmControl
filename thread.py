from wmControl import wlmConst
from wmControl import control
from wmControl import wlmData


class callback:
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
            print(mode)
        except ValueError:
            print(f"{mode} not defined. Version:{ver}, Timestamp?:{int_val}, Measurement?:{double_val}, res1:{result}")

        if (ver == self.version) and (mode in const_to_channel):
            print(
                f"Time:{int_val}, WM:{ver}, Channel:{const_to_channel[mode]}, Wavelength:{299792.458 / double_val:.8f}"
            )

    # Prints all measured wavelengths one WM
    # Unit: nm
    def wavelengthsProcEx(self, ver: int, mode: int, int_val: int, double_val: float, result: int):
        const_to_channel = {
            wlmConst.measure_mode.cmiWavelength1: 1,
            wlmConst.measure_mode.cmiWavelength2: 2,
            wlmConst.measure_mode.cmiWavelength3: 3,
            wlmConst.measure_mode.cmiWavelength4: 4,
            wlmConst.measure_mode.cmiWavelength5: 5,
            wlmConst.measure_mode.cmiWavelength6: 6,
            wlmConst.measure_mode.cmiWavelength7: 7,
            wlmConst.measure_mode.cmiWavelength8: 8,
        }

        if (ver == self.version) and (mode in const_to_channel):
            print(f"Time:{int_val}, WM:{ver}, Channel:{const_to_channel[mode]}, Wavelength:{double_val:.8f}")

    # Prints all measured wavelengths of all WMs connected to the control-PC
    # Unit: nm
    def allwavelengthsProcEx(self, Ver, Mode, IntVal, DblVal, Res1):
        if Mode == wlmConst.cmiWavelength1:
            # print("Time:{}, WM:{}, Channel:1, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength2:
            # print("Time:{}, WM:{}, Channel:2, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength3:
            # print("Time:{}, WM:{}, Channel:3, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength4:
            # print("Time:{}, WM:{}, Channel:4, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength5:
            # print("Time:{}, WM:{}, Channel:5, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength6:
            # print("Time:{}, WM:{}, Channel:6, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength7:
            # print("Time:{}, WM:{}, Channel:7, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])
        if Mode == wlmConst.cmiWavelength8:
            # print("Time:{}, WM:{}, Channel:8, Wavelength:{:.8f}".format(IntVal, Ver, DblVal))
            self.put([IntVal, Ver, DblVal])

    def getSwitchedChannel(self, Ver, Mode, IntVal, DblVal, Res1):
        if Ver == self.version and Mode == wlmConst.cmiSwitcherChannel:
            print(
                f"Time:{Res1}, WM:{Ver}, Active Channel: {IntVal}, Getter-state:{DblVal} Wavelength:{wlmData.dll.GetWavelengthNum(IntVal, 0):.8f}"
            )

    def __init__(self, ver, wavemeter):
        self.version = ver
        self.put = wavemeter.putBfr
