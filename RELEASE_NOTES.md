# DekTec SDK Revision History
## SDK version July 2019

```
Versions DTAPI: v5.35.0.124
Drivers: Dta v4.27.3.259, DtPcie v1.3.0.72, DtaNw v3.5.10.41 , Dtu v4.13.5.82
DtapiService: v3.6.0.81
```

### New features:
- Support for DTA-2132 High-End Satellite Receiver
- Matrix API: Support to receive/transmit raw 4k formats
- DTAPINET now supports DtPcie cards (DTA-2132, DTA-2139B, DTA-2172 and DTA-2175)
- DTA-2115B: Support for the 2 types of noise generators (requires firmware v2)
- DTA-2131: Support for larger ATSC sample rate offsets


### Bug fixes:
-NicInpChannel methods ClearFlags() and GetFlags() were missing
- Modulator cards: noise generation was not working for IQ-direct mode
- DTA-2131: STMP2 RX-mode was missing
- DTA-2131: AdvDemod::OpenStream() function returned unclear error on no license
- DTA-2131: Improved ATSC 3.0 demodulator for adjacent channel interference
- DTA-2136/39: tuner offset for possible lock delay was accidentally removed in SDK Jan2019 release
- DTA-2175: Failsafe functions were not available


### Linux only New features:
- Driver support for linux kernel v5.

## NOTES
Support for DTA-2132 requires Visual Studio 2013 or higher and the DtPcie driver installed.
