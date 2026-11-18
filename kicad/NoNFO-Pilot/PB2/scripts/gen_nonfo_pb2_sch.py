# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_nonfo_pb2_sch.py — NoNFO-Pilot-PB2 schematic generator (sprint S36).

One PocketBeagle 2 Industrial (PB2-I) carries the Pilot and TACCO functions on a
BeagleBone Black outline, architecture B+ (owner decision OD-18, 2026-11-14): a
MSPM0G3519-Q1 trust-module MCU owns CAN-FD, RS-485, the HI-6138 1553 engine, the
write-block PLD inputs, the fan and the Wi-Fi enable, and talks to the PB2-I on SPI0.

Inputs, all in this directory tree:
  * ``sch/ported_blocks.json`` — the Pilot and TACCO blocks, copied by ``port_blocks.py``.
  * ``pin_ledger/`` — the PB2-I header and MCU allocations.  Header and MCU pins are read
    from the solvers, never typed in, so the schematic and the ledger cannot drift.
  * ``docs/BOM.csv`` — the S35 footprint of record for every part number on it.

Every part is a rectangular symbol whose pins carry the OEM data-sheet numbers and names,
each wired to a global net label (the Serenity-UAV Pilot/TACCO generator pattern).  The
emitter functions below are ported from ``Pilot/scripts/gen_pilot_sch.py`` (CC BY 4.0).

New blocks (data sheets in Serenity-UAV ``avionics/datasheets/``):
  * MSPM0G3519-Q1 RGZ-48 [REF-SENSOR-017]: pin numbers from the verified Serenity symbol
    ``MSPM0G3519_Q1_RGZ.kicad_sym``.  Sec 7.3: CVDD 10 uF, CVCORE 470 nF.  Sec 9.1: NRST
    47 k pull-up with 10 nF.  Table 6-4: PA18 (BSL_invoke) must be low at reset.
  * USB2641i-HZH-02 [REF-NFP-014] Fig 4-2 and Table 6-1: 12.0 k 1 % RBIAS, 1 uF on CRFILT
    and PLLFILT, 4.7 uF on VDD33 pins 16 and 48, TEST to ground, VBUS_DET from the host's
    USB1_DRVVBUS (3.3 V, permanently attached host), 24 MHz crystal per sec 10.1.
  * Sterling-LWB5+ 453-00046 [REF-SENSOR-065] pin table: USB/USB strap 000, USB2_RREF
    4.75 k 1 % to ground, VBAT >= 3.6 V so VOUT_3P3 feeds VDDIO_RF and USB2_AVDD33, and an
    external 32.768 kHz LPO on SUSCLK (DVK guide sec 5.3.2: required by standard software).
  * +3V6_WIFI: TPSM82822SILR adjustable [REF-PWR-008] sec 9.2.1.2: R2 100 k, R1 511 k
    (3.67 V), 120 pF feed-forward.  The LWB5+ peak PHY-calibration current, 768 mA, is
    above the TPS63031's 800 mA step-down rating once mLRS and the BT/15.4 module share it.

Author: Claude (Anthropic), 2026-11-18, for S. Griffing (Griffing Technology LLC).
"""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PB2 = Path(__file__).resolve().parents[1]
KIC = PB2 / "kicads"
OUT = KIC / "NoNFO-Pilot-PB2.kicad_sch"
SYMLIB = KIC / "NoNFO-Pilot-PB2.kicad_sym"
LIB = "NoNFO_PB2"
PROJECT = "NoNFO-Pilot-PB2"

SIZE = 1.27
PIN_PITCH = 2.54
STUB = 2.54
_uid = itertools.count(1)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Footprints of record (S35 BOM) and the ones S36 adds.
# ---------------------------------------------------------------------------
def bom_footprints() -> Dict[str, str]:
    rows = csv.DictReader((PB2 / "docs" / "BOM.csv").open(newline=""))
    return {r["mpn"]: r["footprint"] for r in rows if not r["qty"].startswith("~")}


FP_C0201 = "Capacitor_SMD:C_0201_0603Metric"
FP_C0402 = "Capacitor_SMD:C_0402_1005Metric"
FP_C0603 = "Capacitor_SMD:C_0603_1608Metric"
FP_R0201 = "Resistor_SMD:R_0201_0603Metric"
FP_R0402 = "Resistor_SMD:R_0402_1005Metric"
FP_OSC2520 = "Oscillator:Oscillator_SMD_ECS_2520MV-xxx-xx-4Pin_2.5x2.0mm"
FP_XTAL3225 = "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm"
FP_HOLE = "MountingHole:MountingHole_3.2mm_M3_DIN965"
FP_TC2030 = "Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical"

# ---------------------------------------------------------------------------
# Net changes applied to every ported part.  Each one is a merge decision.
# ---------------------------------------------------------------------------
RENAME = {
    # TACCO's SPI0 bus is the same physical PB2-I SPI0 as Pilot's.
    "SPI0_B_CLK": "SPI0_CLK", "SPI0_B_MISO": "SPI0_MISO", "SPI0_B_MOSI": "SPI0_MOSI",
    "SPI0_B_CS_ZB": "SPI0_CS_ZB", "SPI0_B_CS_FLASH": "SPI0_CS_FLASH",
    # B+: the bus transceivers hang off the MCU, not the PB2-I.
    "MCAN0_TX": "MCAN_TX", "MCAN0_RX": "MCAN_RX", "SPI0_CS_1553": "M1553_CSN",
    "FAN_PWM_B": "FAN_PWM",
    # mLRS link: header names from the ledger (PB2-I point of view).
    "UART_WIOE5_TX": "MLRS_UART_TX", "UART_WIOE5_TX_F": "MLRS_UART_TX_F",
    "UART_WIOE5_RX": "MLRS_UART_RX", "UART_WIOE5_RX_F": "MLRS_UART_RX_F",
    # Hub downstream port 2 carries the ring NIC (Pilot fed it straight from USB1).
    "USB1_DP": "HUB_DN2_DP", "USB1_DM": "HUB_DN2_DM",
    "UART_GPS_TX": "GNSS_TXD", "UART_GPS_RX": "GNSS_RXD", "GPS_TIMEPULSE": "GNSS_PPS",
}

# Per-pin changes: (ref, pin) -> net (None = no-connect).
PIN_SET: Dict[Tuple[str, str], Optional[str]] = {
    # HI-6138 host SPI on the MCU's SPI1 (mcu_ledger), not PB2-I SPI0.
    ("1553-XCVR", "17"): "M1553_SCK", ("1553-XCVR", "18"): "M1553_MISO",
    ("1553-XCVR", "19"): "M1553_MOSI",
    # Finding F9: TACCO ties the PB2-I TX to STM32WLE5 PA2, which is USART2_TX
    # [stm32wle5jc.pdf pin table: PA2 USART2_TX, PA3 USART2_RX].  Crossed here.
    ("MLRS-MCU", "9"): "MLRS_UART_RX_F", ("MLRS-MCU", "10"): "MLRS_UART_TX_F",
    # BT UART crossed to the PB2-I's UART2 (ledger: BT_UART_TX = PB2-I TXD).
    ("WIFI-BT-ZB", "49"): "BT_UART_RX", ("WIFI-BT-ZB", "51"): "BT_UART_TX",
    ("WIFI-BT-ZB", "50"): "BT_UART_RTS", ("WIFI-BT-ZB", "52"): "BT_UART_CTS",
    # WIFI_EN now drives the LWB5+; the BT/15.4 module stays powered (PDn pulled up).
    ("WIFI-BT-ZB", "10"): "ZB_PDN",
    # SD_INT is the module's SDIO interrupt; SDIO is not used (UART + SPI host).
    ("WIFI-BT-ZB", "72"): None,
    # GNSS: crossed UART, RESET_N left open (internal pull-up, MAX-M10S Table 10).
    ("GPS", "9"): None,
    # Write-block PLD: I/O 18 drives the hub card reader's SD_WP (OD-23).
    ("SD-WB", "18"): "HUB_SD_WP",
    # microSD on the hub's card reader (OD-23) instead of the AM625 MMC.
    ("J-SD", "1"): "SD_D2", ("J-SD", "2"): "SD_D3", ("J-SD", "3"): "SD_CMD",
    ("J-SD", "4"): "SD_VDD", ("J-SD", "5"): "SD_CLK", ("J-SD", "7"): "SD_D0",
    ("J-SD", "8"): "SD_D1", ("J-SD", "9"): "SD_NCD",
}
# GPS pins by number: 2 TXD -> PB2-I RX, 3 RXD <- PB2-I TX (ledger GNSS_UART_* are PB2-I side).
GPS_UART = {"GNSS_TXD": "GNSS_UART_RX", "GNSS_RXD": "GNSS_UART_TX"}
REF_RENAME = {"J-ANT": "J-ANT-GNSS"}
# Pilot's NIC VBUS sense came from a PB2-I GPIO; behind the hub it only needs the pull-up.
DROP_REFS: set = set()


def ported_parts() -> List[Dict[str, Any]]:
    data = json.loads((PB2 / "sch" / "ported_blocks.json").read_text())
    fps = bom_footprints()
    out = []
    for p in data["parts"]:
        if p["ref"] in DROP_REFS:
            continue
        pins = []
        for pn, fn, net, side in p["pins"]:
            net = RENAME.get(net, net)
            net = GPS_UART.get(net, net)
            if (p["ref"], pn) in PIN_SET:
                net = PIN_SET[(p["ref"], pn)]
            pins.append((pn, fn, net, side))
        q = dict(p, pins=pins, ref=REF_RENAME.get(p["ref"], p["ref"]))
        if q["mpn"] in fps:
            q["fp"] = fps[q["mpn"]]
        out.append(q)
    by = {p["ref"]: p for p in out}
    # TPS63031 on the corrected DSK0010A land: pad 11 is the thermal pad.
    by["U-3V3RF"]["pins"].append(("11", "EP", "GND", "R"))
    by["U-3V3RF"]["fp"] = fps["TPS63031DSKR"]
    # Footprints the BOM names by function rather than part number.
    by["NOR-FLASH"]["fp"] = fps["W25Q128JVSIQ"]
    by["SD-WB"]["mpn"] = "ATF16V8BQL-15XU"
    by["GPS"]["fp"] = fps["MAX-M10S-00B"]
    # Pilot's 742792512 is rated 2 A; the merged 5 V peak is 3.4 A (S36 budget).  TACCO's
    # 742792510 is rated 5 A at a 20 K rise, 30 mOhm max (wurth-742792510.pdf p.1).
    by["FB1"].update(value="742792510", mpn="742792510", mfr="Wurth Elektronik",
                     fp=fps["742792510"], ds="wurth-742792510.pdf p.1: 5 A, 30 mOhm, 70 Ohm at 100 MHz")
    by["SW-MLRS"].update(mpn="KMR211NG LFS", mfr="C&K (Littelfuse)")
    return out


# ---------------------------------------------------------------------------
# PB2-I header from the ledger.  Rail and USB pins come from Pilot's map.
# ---------------------------------------------------------------------------
FIXED_HEADER = {
    "P1": {1: "+5V", 5: "+5V", 9: "USB1_DM", 11: "USB1_DP", 15: "GND", 16: "GND", 22: "GND"},
    "P2": {15: "GND", 21: "GND"},
}


def header_alloc() -> Dict[str, str]:
    led = _load("pin_ledger", PB2 / "pin_ledger" / "pin_ledger.py")
    pins = led.load_pins(PB2 / "pin_ledger" / "AM625_PB2I_header_mux.json")
    dem = json.loads((PB2 / "pin_ledger" / "pb2_net_demand.json").read_text())
    nets = [n for n in dem["nets"] if "B+" in n["arch"]]
    alloc, note = led.solve(pins, nets, dem["reserved_pins"])
    if not alloc:
        raise SystemExit(f"B+ does not fit the header: {note}")
    return {k: v.split()[0] for k, v in alloc.items() if k != "_spare"}


def mcu_alloc() -> Dict[str, str]:
    led = _load("mcu_ledger", PB2 / "pin_ledger" / "mcu_ledger.py")
    mux = json.loads((PB2 / "pin_ledger" / "MSPM0G3519_RGZ48_mux.json").read_text())
    dem = json.loads((PB2 / "pin_ledger" / "mcu_net_demand.json").read_text())
    alloc = led.solve(mux, dem)
    if not alloc:
        raise SystemExit("B+ does not fit the MCU")
    return {k: v for k, v in alloc.items() if k != "_spare"}


def headers(alloc: Dict[str, str]) -> List[Dict[str, Any]]:
    by_pin = {v: k for k, v in alloc.items()}
    out = []
    for rail, fp in (("P1", "Serenity-Custom:PocketBeagle2_2x18_P1_TSM-DV-LC"),
                     ("P2", "Serenity-Custom:PocketBeagle2_2x18_P2_TSM-DV-LC")):
        pins = []
        for i in range(1, 37):
            key = f"{rail}.{i:02d}"
            net = FIXED_HEADER[rail].get(i) or by_pin.get(key)
            pins.append((str(i), key, net, "L" if i <= 18 else "R"))
        out.append({"ref": f"PB2-{rail}", "value": f"PB2I-{rail}-2x18", "fp": fp,
                    "mpn": "TSM-118-04-L-DV-LC", "mfr": "Samtec",
                    "ds": "PB2-I P1/P2 rails; nets from pin_ledger/pin_ledger.py option B+",
                    "pins": pins})
    return out


# MCU port -> RGZ-48 pin number, from Serenity-UAV avionics/kicad/symbols/
# MSPM0G3519_Q1_RGZ.kicad_sym (verified symbol, REF-SENSOR-017 Table 6-2).
MCU_PIN = {
    "PA0": "1", "PA1": "2", "PA28": "3", "PA31": "5", "PA2": "8", "PA3": "9", "PA4": "10",
    "PA5": "11", "PA6": "12", "PA7": "13", "PB2": "14", "PB3": "15", "PA8": "16", "PA9": "17",
    "PA10": "18", "PA11": "19", "PB6": "20", "PB7": "21", "PB8": "22", "PB9": "23",
    "PB14": "24", "PB15": "25", "PB16": "26", "PA12": "27", "PA13": "28", "PA14": "29",
    "PA15": "30", "PA16": "31", "PA17": "32", "PA18": "33", "PA19": "34", "PA20": "35",
    "PB17": "36", "PB18": "37", "PB19": "38", "PA21": "39", "PA22": "40", "PB20": "41",
    "PB24": "42", "PA23": "43", "PA24": "44", "PA25": "45", "PA26": "46", "PA27": "47",
}
# MCU ledger names that are the PB2-I's own SPI0 nets.
MCU_HOST = {"HOST_MISO": "SPI0_MISO", "HOST_SCK": "SPI0_CLK", "HOST_MOSI": "SPI0_MOSI",
            "HOST_CSN": "SPI0_CS_MCU"}


def mcu(alloc: Dict[str, str]) -> Dict[str, Any]:
    port_net = {port.split()[0]: MCU_HOST.get(net, net) for net, port in alloc.items()}
    port_net.update({"PA19": "MCU_SWDIO", "PA20": "MCU_SWCLK", "PA18": "MCU_BSL"})
    pins = [("6", "VDD", "+3V3", "R"), ("7", "VSS", "GND", "R"), ("49", "EP", "GND", "R"),
            ("48", "VCORE", "MCU_VCORE", "R"), ("4", "NRST", "MCU_RSTN", "R")]
    for port, pn in sorted(MCU_PIN.items(), key=lambda kv: int(kv[1])):
        pins.append((pn, port, port_net.get(port), "L"))
    return {"ref": "MCU", "value": "MSPM0G3519-Q1", "fp": "", "mpn": "M0G3519QRGZRQ1",
            "mfr": "Texas Instruments",
            "ds": "SLASFA6B Table 6-2; pins from MSPM0G3519_Q1_RGZ.kicad_sym [REF-SENSOR-017]",
            "pins": pins}


def hub() -> Dict[str, Any]:
    """Microchip USB2641i-HZH-02, DS00001948C Fig 4-2 / Table 6-1 [REF-NFP-014]."""
    nc = None
    t = [
        ("1", "USBDN_DM2", "HUB_DN2_DM"), ("2", "USBDN_DP2", "HUB_DN2_DP"),
        ("3", "USBDN_DM3", "HUB_DN3_DM"), ("4", "USBDN_DP3", "HUB_DN3_DP"),
        ("5", "VDD33", "+3V3"), ("6", "PRTCTL2", nc), ("7", "PRTCTL3", nc),
        ("8", "SPI_CE_n", nc), ("9", "SPI_CLK/SCL", "HUB_SPI_CLK"),
        ("10", "SPI_DO/SDA/SPI_SPD_SEL", nc), ("11", "SPI_DI", nc), ("12", "VDD33", "+3V3"),
        ("13", "SD_WP", "HUB_SD_WP"), ("14", "SD_nCD", "SD_NCD"),
        ("15", "CRFILT", "HUB_CRFILT"), ("16", "VDD33", "+3V3"), ("17", "SD_D1", "SD_D1"),
        ("18", "SD_D0", "SD_D0"), ("19", "SD_D7", nc), ("20", "SD_D6", nc),
        ("21", "SD_CLK", "SD_CLK"), ("22", "NC", nc), ("23", "SD_D5", nc),
        ("24", "SD_CMD", "SD_CMD"), ("25", "VDD33", "+3V3"), ("26", "NC", nc),
        ("27", "NC", nc), ("28", "NC", nc), ("29", "NC", nc), ("30", "SD_D4", nc),
        ("31", "MS_INS", nc), ("32", "SD_D3", "SD_D3"), ("33", "SD_D2", "SD_D2"),
        ("34", "VDD33", "+3V3"), ("35", "CRD_PWR", "SD_VDD"), ("36", "NC", nc),
        ("37", "LED", nc), ("38", "nRESET", "USB_HUB_RSTN"),
        ("39", "VBUS_DET", "USB1_DRVVBUS"), ("40", "TEST", "GND"), ("41", "VDD33", "+3V3"),
        ("42", "USB+", "USB1_DP"), ("43", "USB-", "USB1_DM"), ("44", "XTAL2", "HUB_XO"),
        ("45", "XTAL1(CLKIN)", "HUB_XI"), ("46", "PLLFILT", "HUB_PLLFILT"),
        ("47", "RBIAS", "HUB_RBIAS"), ("48", "VDD33", "+3V3"), ("49", "EP", "GND"),
    ]
    return {"ref": "HUB", "value": "USB2641i-HZH-02", "fp": "", "mpn": "USB2641i-HZH-02",
            "mfr": "Microchip Technology", "ds": "DS00001948C Fig 4-2, Table 6-1 [REF-NFP-014]",
            "pins": [(a, b, c, "L" if int(a) <= 24 else "R") for a, b, c in t]}


def wifi() -> Dict[str, Any]:
    """Ezurio Sterling-LWB5+ 453-00046 (MHF4), data sheet v5.2 pin table [REF-SENSOR-065]."""
    nets = {
        "4": ("STRAP_2", "WIFI_STRAP"), "5": ("STRAP_0", "WIFI_STRAP"),
        "6": ("VOUT_3P3", "WIFI_VOUT3P3"), "7": ("VDDIO_RF", "WIFI_VOUT3P3"),
        "17": ("VBAT", "+3V6_WIFI"), "18": ("VBAT", "+3V6_WIFI"),
        "24": ("USB2_DM", "HUB_DN3_DM"), "25": ("USB2_DP", "HUB_DN3_DP"),
        "26": ("USB2_RREF", "WIFI_RREF"), "28": ("USB2_AVDD33", "WIFI_VOUT3P3"),
        # VDDIO from the module's own VOUT_3P3 so it can never rise before VBAT (sec 6 note).
        "30": ("VDDIO", "WIFI_VOUT3P3"), "33": ("WL_REG_ON", "WIFI_EN"),
        "34": ("SUSCLK", "WIFI_SUSCLK"),
    }
    names = {
        2: "RF_SW_CTRL_5", 3: "RF_SW_CTRL_0", 9: "SDIO_DATA0", 10: "SDIO_DATA1",
        11: "SDIO_DATA3", 12: "SDIO_CMD", 13: "SDIO_DATA2", 15: "SDIO_CLK", 19: "GPIO_4",
        20: "GPIO_6", 21: "GPIO_3", 22: "GPIO_2", 23: "GPIO_5", 31: "GPIO_1",
        32: "BT_REG_ON", 36: "GPIO_0", 37: "BT_DEVICE", 38: "BT_PCM_IN", 39: "BT_PCM_CLK",
        40: "BT_PCM_SYNC", 41: "BT_PCM_OUT", 43: "BT_UART_TXD", 44: "BT_UART_CTSn",
        45: "BT_UART_RXD", 46: "BT_UART_RTSn", 47: "BT_HOST_WAKE", 50: "RF_OUT",
    }
    gnd = {1, 8, 14, 16, 27, 29, 35, 42, 48, 49, 51} | set(range(52, 69))
    pins = []
    for n in range(1, 69):
        if str(n) in nets:
            fn, net = nets[str(n)]
        elif n in gnd:
            fn, net = "GND", "GND"
        else:
            fn, net = names[n], None
        pins.append((str(n), fn, net, "L" if n <= 34 else "R"))
    return {"ref": "WIFI", "value": "LWB5+ 453-00046", "fp": "", "mpn": "453-00046",
            "mfr": "Ezurio", "ds": "Sterling-LWB5+ data sheet v5.2 pin table [REF-SENSOR-065]",
            "pins": pins}


def two(ref, val, fp, a, b, ds, mpn="", mfr="", names=("P", "N"), dnp=False):
    return {"ref": ref, "value": val, "fp": fp, "mpn": mpn, "mfr": mfr, "ds": ds, "dnp": dnp,
            "pins": [("1", names[0], a, "L"), ("2", names[1], b, "R")]}


def new_support() -> List[Dict[str, Any]]:
    C, R = two, two
    s = [
        # --- trust-module MCU --------------------------------------------------
        C("C-MCU-VDD1", "10uF 10V X5R", FP_C0603, "+3V3", "GND", "SLASFA6B sec 7.3 CVDD 10 uF"),
        C("C-MCU-VDD2", "100nF", FP_C0402, "+3V3", "GND", "SLASFA6B sec 9.1 HF bypass"),
        C("C-MCU-VCORE", "470nF", FP_C0402, "MCU_VCORE", "GND", "SLASFA6B sec 7.3 CVCORE 470 nF"),
        R("R-MCU-RST", "47k", FP_R0201, "+3V3", "MCU_RSTN", "SLASFA6B sec 9.1 NRST pull-up", names=("A", "B")),
        C("C-MCU-RST", "10nF", FP_C0201, "MCU_RSTN", "GND", "SLASFA6B sec 9.1 NRST 10 nF"),
        R("R-MCU-BSL", "47k", FP_R0201, "MCU_BSL", "GND",
          "SLASFA6B Table 6-4: BSL_invoke (PA18) low at BOOTRST", names=("A", "B")),
        {"ref": "J-MCU-SWD", "value": "TC2030-IDC-NL pads", "fp": FP_TC2030, "mpn": "",
         "ds": "Tag-Connect TC2030-IDC-NL (no part); MSPM0 SWD", "in_bom": False,
         "pins": [("1", "VTREF", "+3V3", "L"), ("2", "SWDIO", "MCU_SWDIO", "L"),
                  ("3", "nRESET", "MCU_RSTN", "L"), ("4", "SWCLK", "MCU_SWCLK", "R"),
                  ("5", "GND", "GND", "R"), ("6", "SWO", None, "R")]},
        # --- USB hub -----------------------------------------------------------
        R("R-HUB-RBIAS", "12k 1%", FP_R0402, "HUB_RBIAS", "GND", "DS00001948C Table 6-1 RBIAS 12.0 k 1 %", names=("A", "B")),
        C("C-HUB-CRF", "1uF 10V", FP_C0402, "HUB_CRFILT", "GND", "DS00001948C Table 6-1 CRFILT 1 uF"),
        C("C-HUB-PLL", "1uF 10V", FP_C0402, "HUB_PLLFILT", "GND", "DS00001948C Table 6-1 PLLFILT 1 uF"),
        C("C-HUB-V16", "4.7uF 10V X5R", FP_C0603, "+3V3", "GND", "DS00001948C Table 6-1 pin 16 4.7 uF"),
        C("C-HUB-V48", "4.7uF 10V X5R", FP_C0603, "+3V3", "GND", "DS00001948C Table 6-1 pin 48 4.7 uF"),
        C("C-HUB-V05", "100nF", FP_C0402, "+3V3", "GND", "VDD33 pin 5 bypass"),
        C("C-HUB-V12", "100nF", FP_C0402, "+3V3", "GND", "VDD33 pin 12 bypass"),
        C("C-HUB-V25", "100nF", FP_C0402, "+3V3", "GND", "VDD33 pin 25 bypass"),
        C("C-HUB-V34", "100nF", FP_C0402, "+3V3", "GND", "VDD33 pin 34 bypass"),
        C("C-HUB-V41", "100nF", FP_C0402, "+3V3", "GND", "VDD33 pin 41 bypass"),
        {"ref": "Y-HUB", "value": "24MHz CL20pF", "fp": FP_XTAL3225, "mpn": "ECS-240-20-33-AGM-TR",
         "mfr": "ECS Inc.", "ds": "DS00001948C sec 10.1, 24 MHz +/-350 ppm fundamental",
         "pins": [("1", "X1", "HUB_XI", "L"), ("2", "GND", "GND", "L"),
                  ("3", "X2", "HUB_XO", "R"), ("4", "GND", "GND", "R")]},
        C("C-HUB-XI", "33pF C0G", FP_C0402, "HUB_XI", "GND", "Fig 10-2: 2 x (20 - 0) - 4 pF stray -> 36, nearest E12 33 pF"),
        C("C-HUB-XO", "33pF C0G", FP_C0402, "HUB_XO", "GND", "Fig 10-2, as C-HUB-XI"),
        R("R-HUB-SPICLK", "10k", FP_R0201, "HUB_SPI_CLK", "GND",
          "Table 6-1: SPI_CLK driven low during reset (no SPI ROM)", names=("A", "B")),
        R("R-HUB-RST", "100k", FP_R0201, "USB_HUB_RSTN", "GND",
          "holds the hub in reset until the PB2-I drives USB_HUB_RSTN", names=("A", "B")),
        R("R-HUB-VBUS", "100k", FP_R0201, "USB1_DRVVBUS", "GND",
          "VBUS_DET low (no connect) until the host drives USB1_DRVVBUS", names=("A", "B")),
        # --- logging microSD on the hub card reader (OD-23) -------------------
        R("R-SD-CD", "10k", FP_R0201, "+3V3", "SD_NCD", "card-detect pull-up", names=("A", "B")),
        C("C-SD-VDD1", "4.7uF 10V X5R", FP_C0603, "SD_VDD", "GND", "card supply bulk (CRD_PWR, 200 mA)"),
        C("C-SD-VDD2", "100nF", FP_C0402, "SD_VDD", "GND", "card supply bypass"),
        R("R-ZB-PDN", "10k", FP_R0201, "+3V3", "ZB_PDN", "BT/15.4 module PDn held high", names=("A", "B")),
        # --- Wi-Fi module ------------------------------------------------------
        R("R-WIFI-RREF", "4.75k 1%", FP_R0402, "WIFI_RREF", "GND", "LWB5+ pin 26: 4.75 k 1 % to ground (USB)", names=("A", "B")),
        R("R-WIFI-STRAP", "10k", FP_R0201, "WIFI_STRAP", "GND", "CONFIG_HOST = 000 (USB/USB)", names=("A", "B")),
        C("C-WIFI-VB1", "10uF 10V X5R", FP_C0603, "+3V6_WIFI", "GND", "VBAT bulk (value to confirm, S36 open item)"),
        C("C-WIFI-VB2", "100nF", FP_C0402, "+3V6_WIFI", "GND", "VBAT bypass"),
        C("C-WIFI-V33", "1uF 10V", FP_C0402, "WIFI_VOUT3P3", "GND", "VOUT_3P3 decoupling (value to confirm)"),
        {"ref": "X-LPO", "value": "32.768kHz 3.3V CMOS", "fp": FP_OSC2520, "mpn": "",
         "ds": "LWB5+ SUSCLK external LPO (DVK guide sec 5.3.2); MPN to select, S36 open item",
         "pins": [("1", "OE", "+3V3", "L"), ("2", "GND", "GND", "L"),
                  ("3", "OUT", "WIFI_SUSCLK", "R"), ("4", "VDD", "+3V3", "R")]},
        C("C-LPO", "100nF", FP_C0402, "+3V3", "GND", "LPO bypass"),
        # --- +3V6_WIFI: TPSM82822SILR adjustable -----------------------------
        {"ref": "U-3V6", "value": "TPSM82822SILR", "fp": "Serenity-Custom:TI_SIL0010D_uSiP-10_2.0x2.5mm_P0.5mm",
         "mpn": "TPSM82822SILR", "mfr": "Texas Instruments",
         "ds": "SLVSEP0F Table 6-1, sec 9.2.1.2 [REF-PWR-008]",
         "pins": [("1", "VIN", "+5V", "L"), ("2", "VIN", "+5V", "L"), ("3", "EN", "+5V", "L"),
                  ("4", "PG", None, "L"), ("5", "VOUT", "+3V6_WIFI", "R"),
                  ("6", "VOUT", "+3V6_WIFI", "R"), ("7", "VOUT", "+3V6_WIFI", "R"),
                  ("8", "FB", "WIFI_FB", "R"), ("9", "GND", "GND", "L"), ("10", "GND", "GND", "L")]},
        C("C-3V6-IN", "22uF 6.3V X6S", FP_C0603, "+5V", "GND", "as C-3V3-IN [REF-PWR-011]", mpn="MSASJ168BC6226MTNA01", mfr="Taiyo Yuden"),
        C("C-3V6-O1", "22uF 6.3V X6S", FP_C0603, "+3V6_WIFI", "GND", "COUT", mpn="MSASJ168BC6226MTNA01", mfr="Taiyo Yuden"),
        C("C-3V6-O2", "22uF 6.3V X6S", FP_C0603, "+3V6_WIFI", "GND", "COUT, 768 mA calibration peak", mpn="MSASJ168BC6226MTNA01", mfr="Taiyo Yuden"),
        R("R-3V6-FB1", "511k 1%", FP_R0201, "+3V6_WIFI", "WIFI_FB", "R1: 0.6 x (1 + 511/100) = 3.67 V", names=("A", "B")),
        R("R-3V6-FB2", "100k 1%", FP_R0201, "WIFI_FB", "GND", "R2 <= 100 k (sec 9.2.1.2.1)", names=("A", "B")),
        C("C-3V6-FF", "120pF C0G", FP_C0201, "+3V6_WIFI", "WIFI_FB", "C3 feed-forward for R2 = 100 k (sec 9.2.1.2.2)"),
    ]
    s += [{"ref": f"H{i}", "value": "M3 PGND", "fp": FP_HOLE, "mpn": "", "ds": "BeagleBone Black hole pattern",
           "in_bom": False, "pins": [("1", "PAD", "PGND", "L")]} for i in range(1, 5)]
    return s


# ---------------------------------------------------------------------------
# Emitter, ported from Serenity-UAV Pilot/scripts/gen_pilot_sch.py (CC BY 4.0).
# ---------------------------------------------------------------------------
def uid() -> str:
    return f"b5000000-0000-0000-0000-{next(_uid):012d}"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def sanitize(ref: str) -> str:
    return re.sub(r"[^A-Za-z0-9_+.-]", "_", ref)


def pin_def(x: float, y: float, ang: int, pn: str, fn: Optional[str]) -> str:
    etype = "power_in" if fn in ("GND", "EP") else "passive"
    return (f"        (pin {etype} line (at {x:.2f} {y:.2f} {ang}) (length {PIN_PITCH}) "
            f'(name "{esc(fn or "")}" (effects (font (size {SIZE} {SIZE})))) '
            f'(number "{esc(pn)}" (effects (font (size {SIZE} {SIZE})))))')


def lib_symbol(ic: Dict[str, Any]):
    left = [p for p in ic["pins"] if p[3] == "L"]
    right = [p for p in ic["pins"] if p[3] == "R"]
    rows = max(len(left), len(right), 1)
    if len(ic["pins"]) <= 2:
        half_w, half_h = 7.62, 2.54
    else:
        half_h, half_w = (rows * PIN_PITCH) / 2 + PIN_PITCH, 16.51
    libid = f"S_{sanitize(ic['ref'])}"
    s = [
        f'    (symbol "{LIB}:{libid}" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)',
        f'      (property "Reference" "U" (at 0 {half_h + 1.27:.2f} 0) (effects (font (size {SIZE} {SIZE}))))',
        f'      (property "Value" "{esc(ic["value"])}" (at 0 {-half_h - 1.27:.2f} 0) (effects (font (size {SIZE} {SIZE}))))',
        f'      (property "Footprint" "{esc(ic["fp"])}" (at 0 0 0) (effects (font (size {SIZE} {SIZE})) (hide yes)))',
        f'      (property "Datasheet" "{esc(ic["ds"])}" (at 0 0 0) (effects (font (size {SIZE} {SIZE})) (hide yes)))',
        f'      (symbol "{libid}_0_1"',
        f"        (rectangle (start {-half_w:.2f} {half_h:.2f}) (end {half_w:.2f} {-half_h:.2f}) "
        f"(stroke (width 0.2540) (type default)) (fill (type background)))",
        "      )",
        f'      (symbol "{libid}_1_1"',
    ]
    for i, (pn, fn, _n, _) in enumerate(left):
        s.append(pin_def(-half_w - PIN_PITCH, half_h - PIN_PITCH * (i + 1), 0, pn, fn))
    for i, (pn, fn, _n, _) in enumerate(right):
        s.append(pin_def(half_w + PIN_PITCH, half_h - PIN_PITCH * (i + 1), 180, pn, fn))
    s += ["      )", "    )"]
    return "\n".join(s), left, right, half_w, half_h


def wire(x1, y1, x2, y2) -> str:
    return (f"  (wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) "
            f'(stroke (width 0) (type default)) (uuid "{uid()}"))')


def label(net: str, x: float, y: float, ang: int) -> str:
    just = "left" if ang == 0 else "right"
    return (f'  (global_label "{esc(net)}" (shape passive) (at {x:.2f} {y:.2f} {ang}) '
            f'(effects (font (size {SIZE} {SIZE})) (justify {just})) (uuid "{uid()}"))')


def emit_instance(ic, X, Y, left, right, half_w, half_h, sheet) -> List[str]:
    libid = f"S_{sanitize(ic['ref'])}"
    hide = f"(effects (font (size {SIZE} {SIZE})) (hide yes))"
    out = [
        f'  (symbol (lib_id "{LIB}:{libid}") (at {X:.2f} {Y:.2f} 0) (unit 1)',
        f'    (exclude_from_sim no) (in_bom {"yes" if ic.get("in_bom", True) else "no"}) (on_board yes) '
        f'(dnp {"yes" if ic.get("dnp") else "no"}) (uuid "{uid()}")',
        f'    (property "Reference" "{esc(ic["ref"])}" (at {X:.2f} {Y - half_h - 1.27:.2f} 0) (effects (font (size {SIZE} {SIZE}))))',
        f'    (property "Value" "{esc(ic["value"])}" (at {X:.2f} {Y + half_h + 1.27:.2f} 0) (effects (font (size {SIZE} {SIZE}))))',
        f'    (property "Footprint" "{esc(ic["fp"])}" (at {X:.2f} {Y:.2f} 0) {hide})',
        f'    (property "Datasheet" "{esc(ic["ds"])}" (at {X:.2f} {Y:.2f} 0) {hide})',
        f'    (property "MPN" "{esc(ic.get("mpn", ""))}" (at {X:.2f} {Y:.2f} 0) {hide})',
    ]
    if ic.get("mfr"):
        out.append(f'    (property "Manufacturer" "{esc(ic["mfr"])}" (at {X:.2f} {Y:.2f} 0) {hide})')
    for pn, *_ in left + right:
        out.append(f'    (pin "{esc(pn)}" (uuid "{uid()}"))')
    out.append(f'    (instances (project "{PROJECT}" (path "/{sheet}" (reference "{esc(ic["ref"])}") (unit 1))))')
    out.append("  )")
    for side, rows in ((-1, left), (1, right)):
        for i, (pn, fn, net, _) in enumerate(rows):
            cx = X + side * (half_w + PIN_PITCH)
            cy = Y - (half_h - PIN_PITCH * (i + 1))
            if net is None:
                out.append(f'  (no_connect (at {cx:.2f} {cy:.2f}) (uuid "{uid()}"))')
            else:
                out.append(wire(cx, cy, cx + side * STUB, cy))
                out.append(label(net, cx + side * STUB, cy, 0 if side > 0 else 180))
    return out


# Copied verbatim from KiCad 9.0.2 power.kicad_sym so ERC finds no library mismatch.
PWR_FLAG_LIB = """    (symbol "power:PWR_FLAG"
		(power)
		(pin_numbers
			(hide yes)
		)
		(pin_names
			(offset 0)
			(hide yes)
		)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(property "Reference" "#FLG"
			(at 0 1.905 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Value" "PWR_FLAG"
			(at 0 3.81 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" "~"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "ki_keywords" "flag power"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(symbol "PWR_FLAG_0_0"
			(pin power_out line
				(at 0 0 90)
				(length 0)
				(name "~"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
		)
		(symbol "PWR_FLAG_0_1"
			(polyline
				(pts
					(xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)
				)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
		)
		(embedded_fonts no)
	)"""
PWR_FLAG_RAILS = ["GND", "PGND", "GND2_CAN", "GND2_RS485", "GND2_CAN_DCDC", "GND2_RS485_DCDC"]


def emit_pwr_flags(x0: float, y0: float, sheet: str) -> List[str]:
    out = []
    for i, rail in enumerate(PWR_FLAG_RAILS):
        x = x0 + i * 20.32
        out.append(
            f'  (symbol (lib_id "power:PWR_FLAG") (at {x:.2f} {y0:.2f} 0) (unit 1)\n'
            f'    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")\n'
            f'    (property "Reference" "#FLG{i + 1}" (at {x:.2f} {y0 - 2.54:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
            f'    (property "Value" "PWR_FLAG" (at {x:.2f} {y0 - 5.08:.2f} 0) (effects (font (size 1.27 1.27))))\n'
            f'    (instances (project "{PROJECT}" (path "/{sheet}" (reference "#FLG{i + 1}") (unit 1)))))')
        out.append(wire(x, y0, x, y0 + STUB))
        out.append(label(rail, x, y0 + STUB, 270))
    return out


TITLE = """  (title_block
    (title "NoNFO-Pilot-PB2 — merged Pilot + TACCO stern-stack cape")
    (date "2026-11-18")
    (rev "S36")
    (company "Griffing Technology LLC")
    (comment 1 "PocketBeagle 2 Industrial cape on a BeagleBone Black outline, architecture B+")
    (comment 2 "Generated by kicad/NoNFO-Pilot/PB2/scripts/gen_nonfo_pb2_sch.py — edit the generator")
    (comment 3 "Drafted by Claude (Anthropic) for S. Griffing; blocks ported from Serenity-UAV Pilot/TACCO")
    (comment 4 "CERN-OHL-W-2.0; pinouts transcribed from OEM data sheets")
  )"""


def all_parts() -> List[Dict[str, Any]]:
    fps = bom_footprints()
    parts = ported_parts() + headers(header_alloc()) + [mcu(mcu_alloc()), hub(), wifi()]
    parts += new_support()
    for p in parts:
        if not p["fp"] and p["mpn"] in fps:
            p["fp"] = fps[p["mpn"]]
        p["pins"] = [tuple(x) for x in p["pins"]]
    refs = [p["ref"] for p in parts]
    dup = {r for r in refs if refs.count(r) > 1}
    if dup:
        raise SystemExit(f"duplicate references: {sorted(dup)}")
    return parts


def netlist(parts) -> Dict[str, List[Tuple[str, str]]]:
    nets: Dict[str, List[Tuple[str, str]]] = {}
    for p in parts:
        for pn, _fn, net, _ in p["pins"]:
            if net is not None:
                nets.setdefault(net, []).append((p["ref"], pn))
    return nets


def main() -> None:
    parts = all_parts()
    sheet = uid()
    built = [(p, *lib_symbol(p)[1:]) for p in parts]
    doc = ["(kicad_sch (version 20250114) (generator eeschema) (generator_version \"9.0\")",
           f'  (uuid "{uid()}")', '  (paper "A0")', TITLE, "  (lib_symbols", PWR_FLAG_LIB]
    doc += [lib_symbol(p)[0] for p in parts]
    doc.append("  )")
    X0, Y0, DX, YMAX = 76.2, 76.2, 63.5, 800.0
    x, y = X0, Y0
    for p, left, right, hw, hh in built:
        if y + 2 * hh > YMAX and y > Y0:
            x, y = x + DX, Y0
        doc += emit_instance(p, x, y + hh, left, right, hw, hh, sheet)
        y += 2 * hh + 15.24
    doc += emit_pwr_flags(X0, Y0 - 45.72, sheet)
    doc += ['  (sheet_instances (path "/" (page "1")))', ")"]
    KIC.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(doc) + "\n")
    lib = ['(kicad_symbol_lib (version 20241209) (generator "gen_nonfo_pb2_sch.py") (generator_version "9.0")']
    lib += [lib_symbol(p)[0].replace(f'(symbol "{LIB}:', '(symbol "', 1) for p in parts]
    SYMLIB.write_text("\n".join(lib + [")"]) + "\n")
    (KIC / "sym-lib-table").write_text(
        f'(sym_lib_table\n  (version 7)\n  (lib (name "{LIB}")(type "KiCad")(uri "${{KIPRJMOD}}/{SYMLIB.name}")(options "")(descr "generated"))\n'
        '  (lib (name "power")(type "KiCad")(uri "${KICAD9_SYMBOL_DIR}/power.kicad_sym")(options "")(descr "KiCad power symbols"))\n)\n')
    print(f"wrote {OUT.name}: {len(parts)} parts, {sum(len(p['pins']) for p in parts)} pins, "
          f"{len(netlist(parts))} nets, {int((x - X0) / DX) + 1} columns")


if __name__ == "__main__":
    sys.exit(main())
