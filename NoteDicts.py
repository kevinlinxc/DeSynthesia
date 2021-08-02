AtoBflat = 22
BflattoB = 16
BtoC = 31
CtoDflat = 19
DflattoD = 24
DtoEflat = 21
EflattoE = 15
EtoF = 34
FtoGflat = 15
GflattoG = 24
GtoAflat = 20
AflattoA = 20

AtoB = AtoBflat + BflattoB
AtoC = AtoB + BtoC
AtoDflat = AtoC + CtoDflat
AtoD = AtoDflat + DflattoD
AtoEflat = AtoD + DtoEflat
AtoE = AtoEflat + EflattoE
AtoF = AtoE + EtoF
AtoGflat = AtoF + FtoGflat
AtoG = AtoGflat + GflattoG
AtoAflat = AtoG + GtoAflat

A0 = 16
A1 = 275
A2 = 534
A3 = 792
A4 = 1052
A5 = 1311
A6 = 1571
A7 = 1828

RANDOM_PARALLAX_BULLSHIT = 3


def getnotes():
    notes = {
        'A0': A0,
        'Bflat0': A0 + AtoBflat,
        'B0': A0 + AtoB,
        'C1': A0 + AtoC,
        'Dflat1': A0 + AtoDflat,
        'D1': A0 + AtoD,
        'Eflat1': A0 + AtoEflat,
        'E1': A0 + AtoE,
        'F1': A0 + AtoF,
        'Gflat1': A0 + AtoGflat + 1,
        'G1': A0 + AtoG,
        'Aflat1': A0 + AtoAflat,
        'A1': A1,
        'Bflat1': A1 + AtoBflat,
        'B1': A1 + AtoB,
        'C2': A1 + AtoC,
        'Dflat2': A1 + AtoDflat,
        'D2': A1 + AtoD,
        'Eflat2': A1 + AtoEflat + RANDOM_PARALLAX_BULLSHIT,
        'E2': A1 + AtoE,
        'F2': A1 + AtoF,
        'Gflat2': A1 + AtoGflat + RANDOM_PARALLAX_BULLSHIT,
        'G2': A1 + AtoG,
        'Aflat2': A1 + AtoAflat,
        'A2': A2,
        'Bflat2': A2 + AtoBflat,
        'B2': A2 + AtoB,
        'C3': A2 + AtoC + RANDOM_PARALLAX_BULLSHIT,
        'Dflat3': A2 + AtoDflat + RANDOM_PARALLAX_BULLSHIT,
        'D3': A2 + AtoD,
        'Eflat3': A2 + AtoEflat,
        'E3': A2 + AtoE,
        'F3': A2 + AtoF,
        'Gflat3': A2 + AtoGflat,
        'G3': A2 + AtoG,
        'Aflat3': A2 + AtoAflat + 1,
        'A3': A3,
        'Bflat3': A3 + AtoBflat + 2,
        'B3': A3 + AtoB,
        'C4': A3 + AtoC + RANDOM_PARALLAX_BULLSHIT,
        'Dflat4': A3 + AtoDflat + RANDOM_PARALLAX_BULLSHIT,
        'D4': A3 + AtoD,
        'Eflat4': A3 + AtoEflat,
        'E4': A3 + AtoE,
        'F4': A3 + AtoF,
        'Gflat4': A3 + AtoGflat,
        'G4': A3 + AtoG,
        'Aflat4': A3 + AtoAflat,
        'A4': A4,
        'Bflat4': A4 + AtoBflat + RANDOM_PARALLAX_BULLSHIT,
        'B4': A4 + AtoB,
        'C5': A4 + AtoC + RANDOM_PARALLAX_BULLSHIT,
        'Dflat5': A4 + AtoDflat + 1,
        'D5': A4 + AtoD,
        'Eflat5': A4 + AtoEflat,
        'E5': A4 + AtoE,
        'F5': A4 + AtoF,
        'Gflat5': A4 + AtoGflat,
        'G5': A4 + AtoG,
        'Aflat5': A4 + AtoAflat,
        'A5': A5,
        'Bflat5': A5 + AtoBflat,
        'B5': A5 + AtoB,
        'C6': A5 + AtoC,
        'Dflat6': A5 + AtoDflat,
        'D6': A5 + AtoD,
        'Eflat6': A5 + AtoEflat,
        'E6': A5 + AtoE,
        'F6': A5 + AtoF,
        'Gflat6': A5 + AtoGflat,
        'G6': A5 + AtoG,
        'Aflat6': A5 + AtoAflat,
        'A6': A6,
        'Bflat6': A6 + AtoBflat,
        'B6': A6 + AtoB,
        'C7': A6 + AtoC,
        'Dflat7': A6 + AtoDflat,
        'D7': A6 + AtoD,
        'Eflat7': A6 + AtoEflat - RANDOM_PARALLAX_BULLSHIT,
        'E7': A6 + AtoE,
        'F7': A6 + AtoF,
        'Gflat7': A6 + AtoGflat,
        'G7': A6 + AtoG,
        'Aflat7': A6 + AtoAflat,
        'A7': A7,
        'Bflat7': A7 + AtoBflat,
        'B7': A7 + AtoB,
        'C8': A7 + AtoC,
    }
    return notes

def getmidi():
    midi = {
        'A0': 21,
        'Bflat0': 22,
        'B0': 23,
        'C1': 24,
        'Dflat1': 25,
        'D1': 26,
        'Eflat1': 27,
        'E1': 28,
        'F1': 29,
        'Gflat1': 30,
        'G1': 31,
        'Aflat1': 32,
        'A1': 33,
        'Bflat1': 34,
        'B1': 35,
        'C2': 36,
        'Dflat2': 37,
        'D2': 38,
        'Eflat2': 39,
        'E2': 40,
        'F2': 41,
        'Gflat2': 42,
        'G2': 43,
        'Aflat2': 44,
        'A2': 45,
        'Bflat2': 46,
        'B2': 47,
        'C3': 48,
        'Dflat3': 49,
        'D3': 50,
        'Eflat3': 51,
        'E3': 52,
        'F3': 53,
        'Gflat3': 54,
        'G3': 55,
        'Aflat3': 56,
        'A3': 57,
        'Bflat3': 58,
        'B3': 59,
        'C4': 60,
        'Dflat4': 61,
        'D4': 62,
        'Eflat4': 63,
        'E4': 64,
        'F4': 65,
        'Gflat4': 66,
        'G4': 67,
        'Aflat4': 68,
        'A4': 69,
        'Bflat4': 70,
        'B4': 71,
        'C5': 72,
        'Dflat5': 73,
        'D5': 74,
        'Eflat5': 75,
        'E5': 76,
        'F5': 77,
        'Gflat5': 78,
        'G5': 79,
        'Aflat5': 80,
        'A5': 81,
        'Bflat5': 82,
        'B5': 83,
        'C6': 84,
        'Dflat6': 85,
        'D6': 86,
        'Eflat6': 87,
        'E6': 88,
        'F6': 89,
        'Gflat6': 90,
        'G6': 91,
        'Aflat6': 92,
        'A6': 93,
        'Bflat6': 94,
        'B6': 95,
        'C7': 96,
        'Dflat7': 97,
        'D7': 98,
        'Eflat7': 99,
        'E7': 100,
        'F7': 101,
        'Gflat7': 102,
        'G7': 103,
        'Aflat7': 104,
        'A7': 105,
        'Bflat7': 106,
        'B7': 107,
        'C8': 108,
    }
    return midi
