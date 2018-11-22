
// C++ header.
#include <iostream>

// Dektec API.
#include <DTAPI.h>

int
main ()
{
  std::cerr << "Running DekTec device(s) scanner...\n";

  int numHwFuncs = 0;
  DtHwFuncDesc hwFuncs[40];

  DTAPI_RESULT dr = ::DtapiHwFuncScan (sizeof (hwFuncs) / sizeof (hwFuncs[0]), numHwFuncs, hwFuncs);
  if (DTAPI_OK != dr)
  {
    std::cerr << "DtapiHwFuncScan failure\n";
    return -1;
  }

  std::cerr << "Detected " << numHwFuncs << " device(s)\n";

  int idx = 1;
  for (int i = 0; i < numHwFuncs; ++i)
  {
    char szDescription[80];
    char szDescription2[80];

    ::DtapiDtHwFuncDesc2String (&hwFuncs[i], DTAPI_HWF2STR_TYPE_NMB, szDescription, 80);
    ::DtapiDtHwFuncDesc2String (&hwFuncs[i], DTAPI_HWF2STR_ITF_TYPE, szDescription2, 80);

    std::cerr << "  " << idx << ": " << szDescription << " (" << szDescription2 << ")\n";
    ++idx;
  }

  return 0;
}