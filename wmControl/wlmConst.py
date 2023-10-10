#
# wlmData API constants generated from wlmData.h
#
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, IntEnum

# Instantiating Constants for 'RFC' parameter
cInstCheckForWLM = -1
cInstResetCalc = 0
cInstReturnMode = cInstResetCalc
cInstNotification = 1
cInstCopyPattern = 2
cInstCopyAnalysis = cInstCopyPattern
cInstControlWLM = 3
cInstControlDelay = 4
cInstControlPriority = 5

# Notification Constants for 'Mode' parameter
cNotifyInstallCallback = 0
cNotifyRemoveCallback = 1
cNotifyInstallWaitEvent = 2
cNotifyRemoveWaitEvent = 3
cNotifyInstallCallbackEx = 4
cNotifyInstallWaitEventEx = 5

# ResultError Constants of Set...-functions
ResERR_NoErr = 0
ResERR_WlmMissing = -1
ResERR_CouldNotSet = -2
ResERR_ParmOutOfRange = -3
ResERR_WlmOutOfResources = -4
ResERR_WlmInternalError = -5
ResERR_NotAvailable = -6
ResERR_WlmBusy = -7
ResERR_NotInMeasurementMode = -8
ResERR_OnlyInMeasurementMode = -9
ResERR_ChannelNotAvailable = -10
ResERR_ChannelTemporarilyNotAvailable = -11
ResERR_CalOptionNotAvailable = -12
ResERR_CalWavelengthOutOfRange = -13
ResERR_BadCalibrationSignal = -14
ResERR_UnitNotAvailable = -15
ResERR_FileNotFound = -16
ResERR_FileCreation = -17
ResERR_TriggerPending = -18
ResERR_TriggerWaiting = -19
ResERR_NoLegitimation = -20
ResERR_NoTCPLegitimation = -21
ResERR_NotInPulseMode = -22
ResERR_OnlyInPulseMode = -23
ResERR_NotInSwitchMode = -24
ResERR_OnlyInSwitchMode = -25
ResERR_TCPErr = -26


class WavemeterType(Enum):
    lsa = 5
    ws6 = 6
    ws7 = 7
    ws8 = 8


class MeasureMode(IntEnum):
    """
    Mode constants for Callback-Export (CallbackEx) and WaitForWLMEvent-function
    """

    cmiResultMode = 1
    cmiRange = 2
    cmiPulse = 3
    cmiPulseMode = cmiPulse
    cmiWideLine = 4
    cmiWideMode = cmiWideLine
    cmiFast = 5
    cmiFastMode = cmiFast
    cmiExposureMode = 6
    cmiExposureValue1 = 7
    cmiExposureValue2 = 8
    cmiDelay = 9
    cmiShift = 10
    cmiShift2 = 11
    cmiReduce = 12
    cmiReduced = cmiReduce
    cmiScale = 13
    cmiTemperature = 14
    cmiLink = 15
    cmiOperation = 16
    cmiDisplayMode = 17
    cmiPattern1a = 18
    cmiPattern1b = 19
    cmiPattern2a = 20
    cmiPattern2b = 21
    cmiMin1 = 22
    cmiMax1 = 23
    cmiMin2 = 24
    cmiMax2 = 25
    cmiNowTick = 26
    cmiCallback = 27
    cmiFrequency1 = 28
    cmiFrequency2 = 29
    cmiDLLDetach = 30
    cmiVersion = 31
    cmiAnalysisMode = 32
    cmiDeviationMode = 33
    cmiDeviationReference = 34
    cmiDeviationSensitivity = 35
    cmiAppearance = 36
    cmiAutoCalMode = 37
    cmiWavelength1 = 42
    cmiWavelength2 = 43
    cmiLinewidth = 44
    cmiLinewidthMode = 45
    cmiLinkDlg = 56
    cmiAnalysis = 57
    cmiAnalogIn = 66
    cmiAnalogOut = 67
    cmiDistance = 69
    cmiWavelength3 = 90
    cmiWavelength4 = 91
    cmiWavelength5 = 92
    cmiWavelength6 = 93
    cmiWavelength7 = 94
    cmiWavelength8 = 95
    cmiVersion0 = cmiVersion
    cmiVersion1 = 96
    cmiPulseDelay = 99

    cmiDLLAttach = 121
    cmiSwitcherSignal = 123
    cmiSwitcherMode = 124
    cmiExposureValue11 = cmiExposureValue1
    cmiExposureValue12 = 125
    cmiExposureValue13 = 126
    cmiExposureValue14 = 127
    cmiExposureValue15 = 128
    cmiExposureValue16 = 129
    cmiExposureValue17 = 130
    cmiExposureValue18 = 131
    cmiExposureValue21 = cmiExposureValue2
    cmiExposureValue22 = 132
    cmiExposureValue23 = 133
    cmiExposureValue24 = 134
    cmiExposureValue25 = 135
    cmiExposureValue26 = 136
    cmiExposureValue27 = 137
    cmiExposureValue28 = 138
    cmiPatternAverage = 139
    cmiPatternAvg1 = 140
    cmiPatternAvg2 = 141
    cmiAnalogOut1 = cmiAnalogOut
    cmiAnalogOut2 = 142
    cmiMin11 = cmiMin1
    cmiMin12 = 146
    cmiMin13 = 147
    cmiMin14 = 148
    cmiMin15 = 149
    cmiMin16 = 150
    cmiMin17 = 151
    cmiMin18 = 152
    cmiMin21 = cmiMin2
    cmiMin22 = 153
    cmiMin23 = 154
    cmiMin24 = 155
    cmiMin25 = 156
    cmiMin26 = 157
    cmiMin27 = 158
    cmiMin28 = 159
    cmiMax11 = cmiMax1
    cmiMax12 = 160
    cmiMax13 = 161
    cmiMax14 = 162
    cmiMax15 = 163
    cmiMax16 = 164
    cmiMax17 = 165
    cmiMax18 = 166
    cmiMax21 = cmiMax2
    cmiMax22 = 167
    cmiMax23 = 168
    cmiMax24 = 169
    cmiMax25 = 170
    cmiMax26 = 171
    cmiMax27 = 172
    cmiMax28 = 173
    cmiAvg11 = cmiPatternAvg1
    cmiAvg12 = 174
    cmiAvg13 = 175
    cmiAvg14 = 176
    cmiAvg15 = 177
    cmiAvg16 = 178
    cmiAvg17 = 179
    cmiAvg18 = 180
    cmiAvg21 = cmiPatternAvg2
    cmiAvg22 = 181
    cmiAvg23 = 182
    cmiAvg24 = 183
    cmiAvg25 = 184
    cmiAvg26 = 185
    cmiAvg27 = 186
    cmiAvg28 = 187
    cmiPatternAnalysisWritten = 202
    cmiSwitcherChannel = 203
    cmiStartCalibration = 235
    cmiEndCalibration = 236
    cmiAnalogOut3 = 237
    cmiAnalogOut4 = 238
    cmiAnalogOut5 = 239
    cmiAnalogOut6 = 240
    cmiAnalogOut7 = 241
    cmiAnalogOut8 = 242
    cmiIntensity = 251
    cmiPower1 = 267
    cmiPower2 = 268
    cmiPower3 = 269
    cmiPower4 = 270
    cmiPower5 = 271
    cmiPower6 = 272
    cmiPower7 = 273
    cmiPower8 = 274
    cmiActiveChannel = 300
    cmiPIDCourse = 1030
    cmiPIDUseTa = 1031
    cmiPIDUseT = cmiPIDUseTa
    cmiPID_T = 1033
    cmiPID_P = 1034
    cmiPID_I = 1035
    cmiPID_D = 1036
    cmiDeviationSensitivityDim = 1040
    cmiDeviationSensitivityFactor = 1037
    cmiDeviationPolarity = 1038
    cmiDeviationSensitivityEx = 1039
    cmiDeviationUnit = 1041
    cmiDeviationBoundsMin = 1042
    cmiDeviationBoundsMax = 1043
    cmiDeviationRefMid = 1044
    cmiDeviationRefAt = 1045
    cmiPIDConstdt = 1059
    cmiPID_dt = 1060
    cmiPID_AutoClearHistory = 1061
    cmiDeviationChannel = 1063
    cmiPID_ClearHistoryOnRangeExceed = 1069
    cmiAutoCalPeriod = 1120
    cmiAutoCalUnit = 1121
    cmiAutoCalChannel = 1122
    cmiServerInitialized = 1124
    cmiWavelength9 = 1130
    cmiExposureValue19 = 1155
    cmiExposureValue29 = 1180
    cmiMin19 = 1205
    cmiMin29 = 1230
    cmiMax19 = 1255
    cmiMax29 = 1280
    cmiAvg19 = 1305
    cmiAvg29 = 1330
    cmiWavelength10 = 1355
    cmiWavelength11 = 1356
    cmiWavelength12 = 1357
    cmiWavelength13 = 1358
    cmiWavelength14 = 1359
    cmiWavelength15 = 1360
    cmiWavelength16 = 1361
    cmiWavelength17 = 1362
    cmiExternalInput = 1400
    cmiPressure = 1465
    cmiBackground = 1475
    cmiDistanceMode = 1476
    cmiInterval = 1477
    cmiIntervalMode = 1478
    cmiCalibrationEffect = 1480
    cmiLinewidth1 = cmiLinewidth
    cmiLinewidth2 = 1481
    cmiLinewidth3 = 1482
    cmiLinewidth4 = 1483
    cmiLinewidth5 = 1484
    cmiLinewidth6 = 1485
    cmiLinewidth7 = 1486
    cmiLinewidth8 = 1487
    cmiLinewidth9 = 1488
    cmiLinewidth10 = 1489
    cmiLinewidth11 = 1490
    cmiLinewidth12 = 1491
    cmiLinewidth13 = 1492
    cmiLinewidth14 = 1493
    cmiLinewidth15 = 1494
    cmiLinewidth16 = 1495
    cmiLinewidth17 = 1496
    cmiTriggerState = 1497
    cmiDeviceAttach = 1501
    cmiDeviceDetach = 1502
    cmiTimePerMeasurement = 1514
    cmiAutoExpoMin = 1517
    cmiAutoExpoMax = 1518
    cmiAutoExpoStepUp = 1519
    cmiAutoExpoStepDown = 1520
    cmiAutoExpoAtSaturation = 1521
    cmiAutoExpoAtLowSignal = 1522
    cmiAutoExpoFeedback = 1523
    cmiAveragingCount = 1524
    cmiAveragingMode = 1525
    cmiAveragingType = 1526
    cmiNowTick_d = 1527
    cmiAirMode = 1532
    cmiAirTemperature = 1534
    cmiAirPressure = 1535
    cmiAirHumidity = 1536
    cmiAirCO2 = 1651
    cmiSubSnapshotID = 1539
    cmiInternalTriggerRate = 1540
    cmiGain11 = 1541
    cmiGain12 = 1542
    cmiGain13 = 1543
    cmiGain14 = 1544
    cmiGain15 = 1545
    cmiGain16 = 1546
    cmiGain17 = 1547
    cmiGain18 = 1548
    cmiGain19 = 1549
    cmiGain110 = 1550
    cmiGain111 = 1551
    cmiGain112 = 1552
    cmiGain113 = 1553
    cmiGain114 = 1554
    cmiGain115 = 1555
    cmiGain116 = 1556
    cmiGain117 = 1557
    cmiGain21 = 1558
    cmiGain22 = 1559
    cmiGain23 = 1560
    cmiGain24 = 1561
    cmiGain25 = 1562
    cmiGain26 = 1563
    cmiGain27 = 1564
    cmiGain28 = 1565
    cmiGain29 = 1566
    cmiGain210 = 1567
    cmiGain211 = 1568
    cmiGain212 = 1569
    cmiGain213 = 1570
    cmiGain214 = 1571
    cmiGain215 = 1572
    cmiGain216 = 1573
    cmiGain217 = 1574
    cmiGain31 = 1575
    cmiGain32 = 1576
    cmiGain33 = 1577
    cmiGain34 = 1578
    cmiGain35 = 1579
    cmiGain36 = 1580
    cmiGain37 = 1581
    cmiGain38 = 1582
    cmiGain39 = 1583
    cmiGain310 = 1584
    cmiGain311 = 1585
    cmiGain312 = 1586
    cmiGain313 = 1587
    cmiGain314 = 1588
    cmiGain315 = 1589
    cmiGain316 = 1590
    cmiGain317 = 1591
    cmiGain41 = 1592
    cmiGain42 = 1593
    cmiGain43 = 1594
    cmiGain44 = 1595
    cmiGain45 = 1596
    cmiGain46 = 1597
    cmiGain47 = 1598
    cmiGain48 = 1599
    cmiGain49 = 1600
    cmiGain410 = 1601
    cmiGain411 = 1602
    cmiGain412 = 1603
    cmiGain413 = 1604
    cmiGain414 = 1605
    cmiGain415 = 1606
    cmiGain416 = 1607
    cmiGain417 = 1608
    cmiMultimodeLevel1 = 1609
    cmiMultimodeLevel2 = 1610
    cmiMultimodeLevel3 = 1611
    cmiMultimodeLevel4 = 1612
    cmiMultimodeLevel5 = 1613
    cmiMultimodeLevel6 = 1614
    cmiMultimodeLevel7 = 1615
    cmiMultimodeLevel8 = 1616
    cmiMultimodeLevel9 = 1617
    cmiMultimodeLevel10 = 1618
    cmiMultimodeLevel11 = 1619
    cmiMultimodeLevel12 = 1620
    cmiMultimodeLevel13 = 1621
    cmiMultimodeLevel14 = 1622
    cmiMultimodeLevel15 = 1623
    cmiMultimodeLevel16 = 1624
    cmiMultimodeLevel17 = 1625
    cmiFastBasedLinewidthAnalysis = 1630
    cmiMultimodeCount1 = 1633
    cmiMultimodeCount2 = 1634
    cmiMultimodeCount3 = 1635
    cmiMultimodeCount4 = 1636
    cmiMultimodeCount5 = 1637
    cmiMultimodeCount6 = 1638
    cmiMultimodeCount7 = 1639
    cmiMultimodeCount8 = 1640
    cmiMultimodeCount9 = 1641
    cmiMultimodeCount10 = 1642
    cmiMultimodeCount11 = 1643
    cmiMultimodeCount12 = 1644
    cmiMultimodeCount13 = 1645
    cmiMultimodeCount14 = 1646
    cmiMultimodeCount15 = 1647
    cmiMultimodeCount16 = 1648
    cmiMultimodeCount17 = 1649


# Index constants for Get- and SetExtraSetting
cesCalculateLive = 4501

# WLM Control Mode Constants
cCtrlWLMShow = 1
cCtrlWLMHide = 2
cCtrlWLMExit = 3
cCtrlWLMStore = 4
cCtrlWLMCompare = 5
cCtrlWLMWait = 0x0010
cCtrlWLMStartSilent = 0x0020
cCtrlWLMSilent = 0x0040
cCtrlWLMStartDelay = 0x0080

# Operation Mode Constants (for "Operation" and "GetOperationState" functions)
cStop = 0
cAdjustment = 1
cMeasurement = 2

# Base Operation Constants (To be used exclusively, only one of this list at a time,
# but still can be combined with "Measurement Action Addition Constants". See below.)
cCtrlStopAll = cStop
cCtrlStartAdjustment = cAdjustment
cCtrlStartMeasurement = cMeasurement
cCtrlStartRecord = 0x0004
cCtrlStartReplay = 0x0008
cCtrlStoreArray = 0x0010
cCtrlLoadArray = 0x0020

# Additional Operation Flag Constants (combine with "Base Operation Constants" above.)
cCtrlDontOverwrite = 0x0000

cCtrlFileGiven = 0x0000


# Measurement Control Mode Constants
cCtrlMeasDelayRemove = 0
cCtrlMeasDelayGenerally = 1
cCtrlMeasDelayOnce = 2
cCtrlMeasDelayDenyUntil = 3
cCtrlMeasDelayIdleOnce = 4
cCtrlMeasDelayIdleEach = 5
cCtrlMeasDelayDefault = 6

# Measurement Triggering Action Constants
cCtrlMeasurementContinue = 0
cCtrlMeasurementInterrupt = 1
cCtrlMeasurementTriggerPoll = 2
cCtrlMeasurementTriggerSuccess = 3
cCtrlMeasurementEx = 0x0100

# ExposureRange Constants
cExpoMin = 0
cExpoMax = 1
cExpo2Min = 2
cExpo2Max = 3

# Amplitude Constants
cMin1 = 0
cMin2 = 1
cMax1 = 2
cMax2 = 3
cAvg1 = 4
cAvg2 = 5

# Measurement Range Constants
cRange_250_410 = 4
cRange_250_425 = 0
cRange_300_410 = 3
cRange_350_500 = 5
cRange_400_725 = 1
cRange_700_1100 = 2
cRange_800_1300 = 6
cRange_900_1500 = cRange_800_1300
cRange_1100_1700 = 7
cRange_1100_1800 = cRange_1100_1700

# Measurement Range Model Constants
cRangeModelOld = 65535
cRangeModelByOrder = 65534
cRangeModelByWavelength = 65533

# Unit Constants for Get-/SetResultMode, GetLinewidth, Convert... and Calibration
cReturnWavelengthVac = 0
cReturnWavelengthAir = 1
cReturnFrequency = 2
cReturnWavenumber = 3
cReturnPhotonEnergy = 4

# Power Unit Constants
cPower_muW = 0
cPower_dBm = 1

# Source Type Constants for Calibration
cHeNe633 = 0
cHeNe1152 = 0
cNeL = 1
cOther = 2
cFreeHeNe = 3
cSLR1530 = 5

# Unit Constants for autocalibration
cACOnceOnStart = 0
cACMeasurements = 1
cACDays = 2
cACHours = 3
cACMinutes = 4

# ExposureRange Constants
cGetSync = 1
cSetSync = 2

# Pattern- and Analysis Constants
cPatternDisable = 0
cPatternEnable = 1
cAnalysisDisable = cPatternDisable
cAnalysisEnable = cPatternEnable

cSignal1Interferometers = 0
cSignal1WideInterferometer = 1
cSignal1Grating = 1
cSignal2Interferometers = 2
cSignal2WideInterferometer = 3
cSignalAnalysis = 4
cSignalAnalysisX = cSignalAnalysis
cSignalAnalysisY = cSignalAnalysis + 1

# State constants used with AutoExposureSetting functions
cJustStepDown = 0
cRestartAtMinimum = 1
cJustStepUp = 0
cDriveToLevel = 1
cConsiderFeedback = 1
cDontConsiderFeedback = 0

# Options identifiers used with GetOptionInfo
cInfoSwitch = 1
cInfoSwitchChannelsCount = 2
cInfoIntNeonLamp = 11
cInfo2ndExternalPort = 13
cInfoPID = 21
cInfoPIDPortsCount = 22
cInfoPIDPortType = 23
cInfoPIDPortRes = 24
cInfoPIDPortUMin = 25
cInfoPIDPortUMax = 26

# PID type constants
cInfoPIDPortTypeInt = 1
cInfoPIDPortTypeExt = 2
cInfoPIDPortTypeDigi = 3

# State constants used with AveragingSetting functions
cAvrgFloating = 1
cAvrgSucceeding = 2
cAvrgSimple = 0
cAvrgPattern = 1

# Return errorvalues of GetFrequency, GetWavelength, GetWLMVersion and GetOptionInfo
ErrNoValue = 0
ErrNoSignal = -1
ErrBadSignal = -2
ErrLowSignal = -3
ErrBigSignal = -4
ErrWlmMissing = -5
ErrNotAvailable = -6
InfNothingChanged = -7
ErrNoPulse = -8
ErrChannelNotAvailable = -10
ErrDiv0 = -13
ErrOutOfRange = -14
ErrUnitNotAvailable = -15
ErrTCPErr = -26
ErrParameterOutOfRange = -28
ErrMaxErr = ErrParameterOutOfRange

# Return errorvalues of GetTemperature and GetPressure
ErrTemperature = -1000
ErrTempNotMeasured = ErrTemperature + ErrNoValue
ErrTempNotAvailable = ErrTemperature + ErrNotAvailable
ErrTempWlmMissing = ErrTemperature + ErrWlmMissing

# Return errorvalues of GetGain
ErrGain = -1000
ErrGainNotAvailable = ErrGain + ErrNotAvailable
ErrGainWlmMissing = ErrGain + ErrWlmMissing
ErrGainChannelNotAvailable = ErrGain + ErrChannelNotAvailable
ErrGainOutOfRange = ErrGain + ErrOutOfRange
ErrGainParameterOutOfRange = ErrGain + ErrParameterOutOfRange

# Return errorvalues of GetMultimodeInfo
ErrMMI = -1000
ErrMMINotAvailable = ErrMMI + ErrNotAvailable
ErrMMIWlmMissing = ErrMMI + ErrWlmMissing
ErrMMIChannelNotAvailable = ErrMMI + ErrChannelNotAvailable
ErrMMIOutOfRange = ErrMMI + ErrOutOfRange
ErrMMIParameterOutOfRange = ErrMMI + ErrParameterOutOfRange

# Return errorvalues of GetDistance
# real errorvalues are ErrDistance combined with those of GetWavelength
ErrDistance = -1000000000
ErrDistanceNotAvailable = ErrDistance + ErrNotAvailable
ErrDistanceWlmMissing = ErrDistance + ErrWlmMissing

# Return flags of ControlWLMEx in combination with Show or Hide, Wait and Res = 1
class ControlFlags(IntEnum):
    flServerStarted = 0x00000001
    flErrDeviceNotFound = 0x00000002
    flErrDriverError = 0x00000004
    flErrUSBError = 0x00000008
    flErrUnknownDeviceError = 0x00000010
    flErrWrongSN = 0x00000020
    flErrUnknownSN = 0x00000040
    flErrTemperatureError = 0x00000080
    flErrPressureError = 0x00000100
    flErrCancelledManually = 0x00000200
    flErrWLMBusy = 0x00000400
    flErrUnknownError = 0x00001000
    flNoInstalledVersionFound = 0x00002000
    flDesiredVersionNotFound = 0x00004000
    flErrFileNotFound = 0x00008000
    flErrParmOutOfRange = 0x00010000
    flErrCouldNotSet = 0x00020000
    flErrEEPROMFailed = 0x00040000
    flErrFileFailed = 0x00080000
    flDeviceDataNewer = 0x00100000
    flFileDataNewer = 0x00200000
    flErrDeviceVersionOld = 0x00400000
    flErrFileVersionOld = 0x00800000
    flDeviceStampNewer = 0x01000000
    flFileStampNewer = 0x02000000

# Return file info flags of SetOperationFile
flFileInfoDoesntExist = 0x0000
flFileInfoExists = 0x0001
flFileInfoCantWrite = 0x0002
flFileInfoCantRead = 0x0004
flFileInfoInvalidName = 0x0008
cFileParameterError = -1


@dataclass
class DataPackage:
    product_id: int


#######################################################################################################################
# dataclasses for cmi with meaning for DblVal. For more see manual page 61.


@dataclass
class Wavelength(DataPackage):
    """
    The wavelength measured on a channel. Do not directly instantiate this class. Use a sibling to correctly set the
    channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Measured wavelength in nm. Needs to be 8 digits long, no longer. Else there will be pointless data.
    """

    timestamp: int
    value: Decimal
    channel: int

    def __str__(self):
        return f"Wavelength measurement: {self.value:.8f} nm | timestamp {self.timestamp} | channel {self.channel} | wavemeter {self.product_id}."


@dataclass(init=False)
class Wavelength1(Wavelength):
    """Wavelength CH1"""

    mode: MeasureMode = MeasureMode.cmiWavelength1

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=0)


@dataclass(init=False)
class Wavelength2(Wavelength):
    """Wavelength CH2"""

    mode = MeasureMode.cmiWavelength2

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=1)


@dataclass(init=False)
class Wavelength3(Wavelength):
    """Wavelength CH3"""

    mode = MeasureMode.cmiWavelength3

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=2)


@dataclass(init=False)
class Wavelength4(Wavelength):
    """Wavelength CH4"""

    mode = MeasureMode.cmiWavelength4

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=3)


@dataclass(init=False)
class Wavelength5(Wavelength):
    """Wavelength CH5"""

    mode = MeasureMode.cmiWavelength5

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=4)


@dataclass(init=False)
class Wavelength6(Wavelength):
    """Wavelength CH6"""

    mode = MeasureMode.cmiWavelength6

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=5)


@dataclass(init=False)
class Wavelength7(Wavelength):
    """Wavelength CH7"""

    mode = MeasureMode.cmiWavelength7

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=6)


@dataclass(init=False)
class Wavelength8(Wavelength):
    """Wavelength CH8"""

    mode = MeasureMode.cmiWavelength8

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), channel=7)


@dataclass(init=False)
class Temperature(DataPackage):
    """
    The internal temperature in degree Celsius.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Measured temperature in degree Celsius.
    """

    mode = MeasureMode.cmiTemperature

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return (
            f"Temperature measurement: {self.value:.4f} °C | timestamp {self.timestamp} | wavemeter {self.product_id}."
        )


@dataclass(init=False)
class Pressure(DataPackage):
    """
    The ambient air pressure in Pascal.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Measured pressure in Pa.
    """

    mode = MeasureMode.cmiPressure

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val) * 100
        super().__init__(product_id=version)

    def __str__(self):
        return f"Pressure measurement: {self.value:.0f} Pa | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class TimeTick(DataPackage):
    """
    Time correlating to a specific measurement calculation. Represents the interval elapsed since start of the
    measurement.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        The time since the start of the measurement in ?.
    """

    mode = MeasureMode.cmiNowTick_d

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Time Tick: {self.value:.4f}  | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class Distance(DataPackage):
    """
    The distance between signal 1 and 2 in multichannel switch versions with Diff option.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Distance between signal 1 and 2.
    """

    mode = MeasureMode.cmiDistance

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Distance measurement: {self.value} Arb.U. | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class Linewidth(DataPackage):
    """
    The calculated linewidth in nm.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        linewidth in nm.
    """

    mode = MeasureMode.cmiLinewidth

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Linewidth measurement: {self.value} nm | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class AnalogIn(DataPackage):
    """
    The analog input voltage in versions with analog input port.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Analog input in volt.
    """

    mode = MeasureMode.cmiAnalogIn

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Analog input measurement: {self.value} V | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class AnalogOut(DataPackage):
    """
    The analog output voltage in versions with analog output port.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Analog output in volt.
    """

    mode = MeasureMode.cmiAnalogOut

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Analog output measurement: {self.value} V | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass
class PID(DataPackage):
    """
    The P, I, D, T and dt parameters in PID regulation versions.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Value of the parameter.
    """

    timestamp: int
    value: Decimal
    parameter: str

    def __str__(self):
        return f"PID measurement: {self.value} Arb.U. | timestamp {self.timestamp} | parameter {self.parameter} | wavemeter {self.product_id}."


@dataclass(init=False)
class PID_P(PID):
    """The P parameter in PID regulation versions."""

    mode = MeasureMode.cmiPID_P

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), parameter="P")


@dataclass(init=False)
class PID_I(PID):
    """The I parameter in PID regulation versions."""

    mode = MeasureMode.cmiPID_I

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), parameter="I")


@dataclass(init=False)
class PID_D(PID):
    """The D parameter in PID regulation versions."""

    mode = MeasureMode.cmiPID_D

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), parameter="D")


@dataclass(init=False)
class PID_T(PID):
    """The T parameter in PID regulation versions."""

    mode = MeasureMode.cmiPID_T

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), parameter="T")


@dataclass(init=False)
class PID_dt(PID):
    """The dt parameter in PID regulation versions."""

    mode = MeasureMode.cmiPID_dt

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        super().__init__(product_id=version, timestamp=int_val, value=Decimal(double_val), parameter="dt")


@dataclass(init=False)
class ExternalInput(DataPackage):
    """
    External user input transferred to the wavemeter (64 possible). Meant to control wavemeter via a client.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        External input.
    """

    mode = MeasureMode.cmiExternalInput

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"External input measurement: {self.value} Arb.U. | timestamp {self.timestamp} | wavemeter {self.product_id}."


@dataclass(init=False)
class DeviationSensitivityFactor(DataPackage):
    """
    Sensitivity prefactor in Laser and PID versions.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    timestamp : int
        Timestamp of the measurement in milliseconds.
    value : Decimal
        Deviation sensitivity factor.
    """

    mode = MeasureMode.cmiDeviationSensitivityFactor

    timestamp: int
    value: Decimal

    def __init__(self, version, int_val, double_val, *_args, **_kwargs):
        self.timestamp = int_val
        self.value = Decimal(double_val)
        super().__init__(product_id=version)

    def __str__(self):
        return f"Deviation sensitivity factor measurement: {self.value} Arb.U. | timestamp {self.timestamp} | wavemeter {self.product_id}."


#######################################################################################################################
# Dataclasses for cmi with meaning for IntVal. For more see manual page 61.
# Use documentation with caution.


@dataclass(init=False)
class FastMode(DataPackage):
    """
    In fast mode the pattern is drawn a little bit faster.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Fast mode state of the wavemeter. Attribute may 0 or 1. 1 mean fast mode is active.
    """

    mode = MeasureMode.cmiFastMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Fast mode active: {bool(self.value)} | wavemeter {self.product_id}."


@dataclass(init=False)
class WideMode(DataPackage):
    """
    Wide mode represent the measurement precision mode indicator.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Wide mode state of the wavemeter. Attribute may 0, 1 or 2. 1 represent wide mode. 2 represent grating analysis.
    """

    mode = MeasureMode.cmiWideMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Wide mode: mode {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class ResultMode(DataPackage):
    """
    Result mode represent the measurement unit.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Unit of the measurement.
    """

    mode = MeasureMode.cmiResultMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Result mode: unit {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class ExposureMode(DataPackage):
    """
    Exposure mode gives hint about automatic exposure control.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        State of the automatic exposure control. Either 0 or 1. 1 if automatic control is active.
    """

    mode = MeasureMode.cmiExposureMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Automatic exposure control active: bool({self.value}) | wavemeter {self.product_id}."


@dataclass(init=False)
class Range(DataPackage):
    """
    Range represent the range in which the wavemeter is operating.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Measurement range of the wavemeter.
    """

    mode = MeasureMode.cmiRange

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Wavemeter range: range {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class PulseMode(DataPackage):
    """
    Pulse mode represent the pulse mode setting.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Pulse mode of the wavemeter. Either 0, 1 or 2. 0 is continuous mode, 1 is standard, single and internally triggered pulsed mode and
        2 is double and externally triggered pulsed mode.
    """

    mode = MeasureMode.cmiPulseMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Pulse mode: mode {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class DisplayMode(DataPackage):
    """
    Represents the display mode settings.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Display mode settings. Either 0 or 1. 1 if the signal are to be drawn.
    """

    mode = MeasureMode.cmiDisplayMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Display mode: mode {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class Reduced(DataPackage):
    """
    Represents the reduction state.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Reduction state. 1 if reduction is active.
    """

    mode = MeasureMode.cmiReduced

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Reduction state: state {bool(self.value)} | wavemeter {self.product_id}."


@dataclass(init=False)
class Link(DataPackage):
    """
    Represents the link state with a COM port.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Link state with a COM port. If the wavemeter is connected with a COM port this 1 else 0.
    """

    mode = MeasureMode.cmiLink

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Link state: connected to COM port {bool(self.value)} | wavemeter {self.product_id}."


@dataclass(init=False)
class Operation(DataPackage):
    """
    Represent the operation state the wavemeter has.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : OperationMode
        Operation state of the wavemeter. cAdjustment means the wavemeter is adjusting,
        cMeasurement means it is measuring, recording or replaying else cStop.
    """

    mode = MeasureMode.cmiOperation

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Operation state: state {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class AnalysisMode(DataPackage):
    """
    Represent the analysis mode state.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Analysis mode of the wavemeter. Either 0 or 1. 1 if analysis mode is active.
    """

    mode = MeasureMode.cmiAnalysisMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Analysis mode state: state {bool(self.value)} | wavemeter {self.product_id}."


@dataclass(init=False)
class SwitcherMode(DataPackage):
    """
    Represent the switcher mode state.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Switcher mode of the wavemeter. Either 0 or 1. 1 if switcher mode is active.
    """

    mode = MeasureMode.cmiSwitcherMode

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Switcher mode state: state {bool(self.value)} | wavemeter {self.product_id}."


@dataclass(init=False)
class SwitcherChannel(DataPackage):
    """
    Represent the current active switcher channel.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Active switcher channel of the wavemeter.
    """

    mode = MeasureMode.cmiSwitcherChannel
    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val - 1
        super().__init__(product_id=version)

    def __str__(self):
        return f"Active switcher channel: channel {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class PIDCourse(DataPackage):
    """
    Represent the current active switcher channel.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : ResultErrorMode
        State of the PID course. Either ResERR_NoErr, ResERR_WlmMissing or ResERR_ParmOutOfRange.
    """

    mode = MeasureMode.cmiPIDCourse

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"PID course state: {self.value} | wavemeter {self.product_id}."


@dataclass(init=False)
class DeviationSensitivityDim(DataPackage):
    """
    Represent the dimension of the .

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : int
        Dimension of the sensitivity of the deviation.
    """

    mode = MeasureMode.cmiDeviationSensitivityDim

    value: int

    def __init__(self, version, int_val, *_args, **_kwargs):
        self.value = int_val
        super().__init__(product_id=version)

    def __str__(self):
        return f"Deviation sensitivity: dimension {self.value} | wavemeter {self.product_id}."


@dataclass
class Min(DataPackage):
    """
    The minimum of a measured interference pattern on a channel. For wavemeter with two CCDs there will be two minimums. See also manual
    page 73 GetAmplitudeNum. Do not directly instantiate this class. Use a sibling to correctly set the channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : Decimal
        The absolut minimum of the interference pattern.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    ccd_array : int
        Index of the CCD array that measured the interference pattern.
    """

    value: Decimal
    channel: int
    ccd_array: int

    def __str__(self):
        return f"Minimum measurement: {self.value} Arb.U. | channel {self.channel} | ccd {self.ccd_array} | wavemeter {self.product_id}."


@dataclass(init=False)
class Min1(Min):
    """The interference pattern minimum of channel 1 for first CCD."""

    mode = MeasureMode.cmiMin1

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Min2(Min):
    """The interference pattern minimum of channel 1 for second CCD."""

    mode = MeasureMode.cmiMin2

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Min11(Min):
    """The interference pattern minimum of channel 1 for first CCD."""

    mode = MeasureMode.cmiMin11

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Min12(Min):
    """The interference pattern minimum of channel 2 for first CCD."""

    mode = MeasureMode.cmiMin12

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=0)


@dataclass(init=False)
class Min13(Min):
    """The interference pattern minimum of channel 3 for first CCD."""

    mode = MeasureMode.cmiMin13

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=0)


@dataclass(init=False)
class Min14(Min):
    """The interference pattern minimum of channel 4 for first CCD."""

    mode = MeasureMode.cmiMin14

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=0)


@dataclass(init=False)
class Min15(Min):
    """The interference pattern minimum of channel 5 for first CCD."""

    mode = MeasureMode.cmiMin15

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=0)


@dataclass(init=False)
class Min16(Min):
    """The interference pattern minimum of channel 6 for first CCD."""

    mode = MeasureMode.cmiMin16

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=0)


@dataclass(init=False)
class Min17(Min):
    """The interference pattern minimum of channel 7 for first CCD."""

    mode = MeasureMode.cmiMin17

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=0)


@dataclass(init=False)
class Min18(Min):
    """The interference pattern minimum of channel 8 for first CCD."""

    mode = MeasureMode.cmiMin18

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=0)


@dataclass(init=False)
class Min19(Min):
    """The interference pattern minimum of some channel for first CCD."""

    mode = MeasureMode.cmiMin19

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=0)


@dataclass(init=False)
class Min21(Min):
    """The interference pattern minimum of channel 1 for second CCD."""

    mode = MeasureMode.cmiMin21

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Min22(Min):
    """The interference pattern minimum of channel 2 for second CCD."""

    mode = MeasureMode.cmiMin22

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=1)


@dataclass(init=False)
class Min23(Min):
    """The interference pattern minimum of channel 3 for second CCD."""

    mode = MeasureMode.cmiMin23

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=1)


@dataclass(init=False)
class Min24(Min):
    """The interference pattern minimum of channel 4 for second CCD."""

    mode = MeasureMode.cmiMin24

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=1)


@dataclass(init=False)
class Min25(Min):
    """The interference pattern minimum of channel 5 for second CCD."""

    mode = MeasureMode.cmiMin25

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=1)


@dataclass(init=False)
class Min26(Min):
    """The interference pattern minimum of channel 6 for second CCD."""

    mode = MeasureMode.cmiMin26

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=1)


@dataclass(init=False)
class Min27(Min):
    """The interference pattern minimum of channel 7 for second CCD."""

    mode = MeasureMode.cmiMin27

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=1)


@dataclass(init=False)
class Min28(Min):
    """The interference pattern minimum of channel 8 for second CCD."""

    mode = MeasureMode.cmiMin28

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=1)


@dataclass(init=False)
class Min29(Min):
    """The interference pattern minimum of some channel for second CCD."""

    mode = MeasureMode.cmiMin29

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=1)


@dataclass
class Max(DataPackage):
    """
    The maximum of a measured interference pattern on a channel. For wavemeter with two CCDs there will be two maximums. See also manual
    page 73 GetAmplitudeNum. Do not directly instantiate this class. Use a sibling to correctly set the channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : Decimal
        The absolut maximum of the interference pattern.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    ccd_array : int
        Index of the CCD array that measured the interference pattern.
    """

    value: Decimal
    channel: int
    ccd_array: int

    def __str__(self):
        return f"Maximum measurement: {self.value} Arb.U. | channel {self.channel} | ccd {self.ccd_array} | wavemeter {self.product_id}."


@dataclass(init=False)
class Max1(Max):
    """The interference pattern maximum of channel 1 for first CCD."""

    mode = MeasureMode.cmiMax1

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Max2(Max):
    """The interference pattern maximum of channel 1 for second CCD."""

    mode = MeasureMode.cmiMax2

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Max11(Max):
    """The interference pattern maximum of channel 1 for first CCD."""

    mode = MeasureMode.cmiMax11

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Max12(Max):
    """The interference pattern maximum of channel 2 for first CCD."""

    mode = MeasureMode.cmiMax12

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=0)


@dataclass(init=False)
class Max13(Max):
    """The interference pattern maximum of channel 3 for first CCD."""

    mode = MeasureMode.cmiMax13

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=0)


@dataclass(init=False)
class Max14(Max):
    """The interference pattern maximum of channel 4 for first CCD."""

    mode = MeasureMode.cmiMax14

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=0)


@dataclass(init=False)
class Max15(Max):
    """The interference pattern maximum of channel 5 for first CCD."""

    mode = MeasureMode.cmiMax15

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=0)


@dataclass(init=False)
class Max16(Max):
    """The interference pattern maximum of channel 6 for first CCD."""

    mode = MeasureMode.cmiMax16

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=0)


@dataclass(init=False)
class Max17(Max):
    """The interference pattern maximum of channel 7 for first CCD."""

    mode = MeasureMode.cmiMax17

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=0)


@dataclass(init=False)
class Max18(Max):
    """The interference pattern maximum of channel 8 for first CCD."""

    mode = MeasureMode.cmiMax18

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=0)


@dataclass(init=False)
class Max19(Max):
    """The interference pattern maximum of some channel for first CCD."""

    mode = MeasureMode.cmiMax19

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=0)


@dataclass(init=False)
class Max21(Max):
    """The interference pattern maximum of channel 1 for second CCD."""

    mode = MeasureMode.cmiMax21

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Max22(Max):
    """The interference pattern maximum of channel 2 for second CCD."""

    mode = MeasureMode.cmiMax22

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=1)


@dataclass(init=False)
class Max23(Max):
    """The interference pattern maximum of channel 3 for second CCD."""

    mode = MeasureMode.cmiMax23

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=1)


@dataclass(init=False)
class Max24(Max):
    """The interference pattern maximum of channel 4 for second CCD."""

    mode = MeasureMode.cmiMax24

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=1)


@dataclass(init=False)
class Max25(Max):
    """The interference pattern maximum of channel 5 for second CCD."""

    mode = MeasureMode.cmiMax25

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=1)


@dataclass(init=False)
class Max26(Max):
    """The interference pattern maximum of channel 6 for second CCD."""

    mode = MeasureMode.cmiMax26

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=1)


@dataclass(init=False)
class Max27(Max):
    """The interference pattern maximum of channel 7 for second CCD."""

    mode = MeasureMode.cmiMax27

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=1)


@dataclass(init=False)
class Max28(Max):
    """The interference pattern maximum of channel 8 for second CCD."""

    mode = MeasureMode.cmiMax28

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=1)


@dataclass(init=False)
class Max29(Max):
    """The interference pattern maximum of some channel for second CCD."""

    mode = MeasureMode.cmiMax29

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=1)


@dataclass
class Avg(DataPackage):
    """
    The average of a measured interference pattern on a channel. For wavemeter with two CCDs there will be two averages. See also manual
    page 73 GetAmplitudeNum. Do not directly instantiate this class. Use a sibling to correctly set the channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : Decimal
        The averages height of the fringes of the interference pattern.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    ccd_array : int
        Index of the CCD array that measured the interference pattern.
    """

    value: Decimal
    channel: int
    ccd_array: int

    def __str__(self):
        return f"Average measurement: {self.value} Arb.U. | channel {self.channel} | ccd {self.ccd_array} | wavemeter {self.product_id}."


@dataclass(init=False)
class Avg1(Avg):
    """The interference pattern average of channel 1 for first CCD."""

    mode = MeasureMode.cmiPatternAvg1

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Avg2(Avg):
    """The interference pattern average of channel 1 for second CCD."""

    mode = MeasureMode.cmiPatternAvg2

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Avg11(Avg):
    """The interference pattern average of channel 1 for first CCD."""

    mode = MeasureMode.cmiAvg11

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=0)


@dataclass(init=False)
class Avg12(Avg):
    """The interference pattern average of channel 2 for first CCD."""

    mode = MeasureMode.cmiAvg12

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=0)


@dataclass(init=False)
class Avg13(Avg):
    """The interference pattern average of channel 3 for first CCD."""

    mode = MeasureMode.cmiAvg13

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=0)


@dataclass(init=False)
class Avg14(Avg):
    """The interference pattern average of channel 4 for first CCD."""

    mode = MeasureMode.cmiAvg14

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=0)


@dataclass(init=False)
class Avg15(Avg):
    """The interference pattern average of channel 5 for first CCD."""

    mode = MeasureMode.cmiAvg15

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=0)


@dataclass(init=False)
class Avg16(Avg):
    """The interference pattern average of channel 6 for first CCD."""

    mode = MeasureMode.cmiAvg16

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=0)


@dataclass(init=False)
class Avg17(Avg):
    """The interference pattern average of channel 7 for first CCD."""

    mode = MeasureMode.cmiAvg17

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=0)


@dataclass(init=False)
class Avg18(Avg):
    """The interference pattern average of channel 8 for first CCD."""

    mode = MeasureMode.cmiAvg18

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=0)


@dataclass(init=False)
class Avg19(Avg):
    """The interference pattern average of some channel for first CCD."""

    mode = MeasureMode.cmiAvg19

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=0)


@dataclass(init=False)
class Avg21(Avg):
    """The interference pattern average of channel 1 for second CCD."""

    mode = MeasureMode.cmiAvg21

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=0, ccd_array=1)


@dataclass(init=False)
class Avg22(Avg):
    """The interference pattern average of channel 2 for second CCD."""

    mode = MeasureMode.cmiAvg22

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=1)


@dataclass(init=False)
class Avg23(Avg):
    """The interference pattern average of channel 3 for second CCD."""

    mode = MeasureMode.cmiAvg23

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=1)


@dataclass(init=False)
class Avg24(Avg):
    """The interference pattern average of channel 4 for second CCD."""

    mode = MeasureMode.cmiAvg24

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=1)


@dataclass(init=False)
class Avg25(Avg):
    """The interference pattern average of channel 5 for second CCD."""

    mode = MeasureMode.cmiAvg25

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=1)


@dataclass(init=False)
class Avg26(Avg):
    """The interference pattern average of channel 6 for second CCD."""

    mode = MeasureMode.cmiAvg26

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=1)


@dataclass(init=False)
class Avg27(Avg):
    """The interference pattern average of channel 7 for second CCD."""

    mode = MeasureMode.cmiAvg27

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=1)


@dataclass(init=False)
class Avg28(Avg):
    """The interference pattern average of channel 8 for second CCD."""

    mode = MeasureMode.cmiAvg28

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=1)


@dataclass(init=False)
class Avg29(Avg):
    """The interference pattern average of some channel for second CCD."""

    mode = MeasureMode.cmiAvg29

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=1)


@dataclass
class Exposure(DataPackage):
    """
    The actual valid exposure value on a channel. For wavemeter with two CCDs there will be two averages. See also manual
    page 90 GetExposureNum. Do not directly instantiate this class. Use a sibling to correctly set the channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : Decimal
        The averages height of the fringes of the interference pattern.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    ccd_array : int
        Index of the CCD array that measured the interference pattern.
    """

    value: Decimal
    channel: int
    ccd_array: int

    def __str__(self):
        return f"Exposure measurement: exposure {self.value} Arb.U. | channel {self.channel} | ccd {self.ccd_array} | wavemeter {self.product_id}."


@dataclass(init=False)
class Exposure1(Exposure):
    """The exposure of channel 1 for first CCD."""

    mode = MeasureMode.cmiExposureValue1

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=1)


@dataclass(init=False)
class Exposure2(Exposure):
    """The exposure of channel 1 for second CCD."""

    mode = MeasureMode.cmiExposureValue2

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=2)


@dataclass(init=False)
class Exposure11(Exposure):
    """The exposure of channel 1 for first CCD."""

    mode = MeasureMode.cmiExposureValue11

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=1)


@dataclass(init=False)
class Exposure12(Exposure):
    """The exposure of channel 2 for first CCD."""

    mode = MeasureMode.cmiExposureValue12

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=1)


@dataclass(init=False)
class Exposure13(Exposure):
    """The exposure of channel 3 for first CCD."""

    mode = MeasureMode.cmiExposureValue13

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=1)


@dataclass(init=False)
class Exposure14(Exposure):
    """The exposure of channel 4 for first CCD."""

    mode = MeasureMode.cmiExposureValue14

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=1)


@dataclass(init=False)
class Exposure15(Exposure):
    """The exposure of channel 5 for first CCD."""

    mode = MeasureMode.cmiExposureValue15

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=1)


@dataclass(init=False)
class Exposure16(Exposure):
    """The exposure of channel 6 for first CCD."""

    mode = MeasureMode.cmiExposureValue16

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=1)


@dataclass(init=False)
class Exposure17(Exposure):
    """The exposure of channel 7 for first CCD."""

    mode = MeasureMode.cmiExposureValue17

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=1)


@dataclass(init=False)
class Exposure18(Exposure):
    """The exposure of channel 8 for first CCD."""

    mode = MeasureMode.cmiExposureValue18

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=1)


@dataclass(init=False)
class Exposure21(Exposure):
    """The exposure of channel 1 for second CCD."""

    mode = MeasureMode.cmiExposureValue21

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1, ccd_array=2)


@dataclass(init=False)
class Exposure22(Exposure):
    """The exposure of channel 2 for second CCD."""

    mode = MeasureMode.cmiExposureValue22

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2, ccd_array=2)


@dataclass(init=False)
class Exposure23(Exposure):
    """The exposure of channel 3 for second CCD."""

    mode = MeasureMode.cmiExposureValue23

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3, ccd_array=2)


@dataclass(init=False)
class Exposure24(Exposure):
    """The exposure of channel 4 for second CCD."""

    mode = MeasureMode.cmiExposureValue24

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4, ccd_array=2)


@dataclass(init=False)
class Exposure25(Exposure):
    """The exposure of channel 5 for second CCD."""

    mode = MeasureMode.cmiExposureValue25

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5, ccd_array=2)


@dataclass(init=False)
class Exposure26(Exposure):
    """The exposure of channel 6 for second CCD."""

    mode = MeasureMode.cmiExposureValue26

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6, ccd_array=2)


@dataclass(init=False)
class Exposure27(Exposure):
    """The exposure of channel 7 for second CCD."""

    mode = MeasureMode.cmiExposureValue27

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7, ccd_array=2)


@dataclass(init=False)
class Exposure28(Exposure):
    """The exposure of channel 8 for second CCD."""

    mode = MeasureMode.cmiExposureValue28

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8, ccd_array=2)


@dataclass
class Power(DataPackage):
    """
    The measured signal power in microwatt of the current shot. See also manual page 71 GetPowerNum.
    Do not directly instantiate this class. Use a sibling to correctly set the channel and mode enum.

    Attributes
    ----------
    product_id : int
        Product id (version) of the WM. Might be a serial number. Do not count on it though.
    value : Decimal
        The power of the current measurement shot.
    channel : int
        Channel of the wavemeter. The channel is a 0 based index.
    """

    value: Decimal
    channel: int

    def __str__(self):
        return f"Power measurement: power {self.value} µW | channel {self.channel} | wavemeter {self.product_id}."


@dataclass(init=False)
class Power1(Power):
    """The power of channel 1."""

    mode = MeasureMode.cmiPower1

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=1)


@dataclass(init=False)
class Power2(Power):
    """The power of channel 2."""

    mode = MeasureMode.cmiPower2

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=2)


@dataclass(init=False)
class Power3(Power):
    """The power of channel 3."""

    mode = MeasureMode.cmiPower3

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=3)


@dataclass(init=False)
class Power4(Power):
    """The power of channel 4."""

    mode = MeasureMode.cmiPower4

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=4)


@dataclass(init=False)
class Power5(Power):
    """The power of channel 5."""

    mode = MeasureMode.cmiPower5

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=5)


@dataclass(init=False)
class Power6(Power):
    """The power of channel 6."""

    mode = MeasureMode.cmiPower6

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=6)


@dataclass(init=False)
class Power7(Power):
    """The power of channel 7."""

    mode = MeasureMode.cmiPower7

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=7)


@dataclass(init=False)
class Power8(Power):
    """The power of channel 8."""

    mode = MeasureMode.cmiPower8

    def __init__(self, version, int_val, *_args, **_kwargs):
        super().__init__(product_id=version, value=Decimal(int_val), channel=8)


class WavemeterException(Exception):
    pass


class ResourceNotAvailable(WavemeterException):
    pass


class NoWavemeterAvailable(WavemeterException):
    pass


class LowSignalError(WavemeterException):
    pass


class NoValueError(WavemeterException):
    pass


wavemeter_exceptions = {
    ErrNoValue: NoValueError,
    ErrLowSignal: LowSignalError,
    ErrWlmMissing: NoWavemeterAvailable,
    ResERR_NotAvailable: ResourceNotAvailable,
}
