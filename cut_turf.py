#!/usr/bin/python3.7

import csv
import sys
import re
import os

WARDS = ["BEXLEY 01",
"BEXLEY 02",
"BEXLEY 03",
"BEXLEY 04",
"BLENDON",
"BROWN",
"CANAL WINCHESTER",
"CLINTON",
"COLUMBUS 01",
"COLUMBUS 02",
"COLUMBUS 03",
"COLUMBUS 04",
"COLUMBUS 05",
"COLUMBUS 06",
"COLUMBUS 07",
"COLUMBUS 08",
"COLUMBUS 09",
"COLUMBUS 10",
"COLUMBUS 11",
"COLUMBUS 12",
"COLUMBUS 13",
"COLUMBUS 14",
"COLUMBUS 15",
"COLUMBUS 16",
"COLUMBUS 17",
"COLUMBUS 18",
"COLUMBUS 19",
"COLUMBUS 20",
"COLUMBUS 21",
"COLUMBUS 22",
"COLUMBUS 23",
"COLUMBUS 24",
"COLUMBUS 25",
"COLUMBUS 26",
"COLUMBUS 27",
"COLUMBUS 28",
"COLUMBUS 29",
"COLUMBUS 30",
"COLUMBUS 31",
"COLUMBUS 32",
"COLUMBUS 33",
"COLUMBUS 34",
"COLUMBUS 35",
"COLUMBUS 36",
"COLUMBUS 37",
"COLUMBUS 38",
"COLUMBUS 39",
"COLUMBUS 40",
"COLUMBUS 41",
"COLUMBUS 42",
"COLUMBUS 43",
"COLUMBUS 44",
"COLUMBUS 45",
"COLUMBUS 46",
"COLUMBUS 47",
"COLUMBUS 48",
"COLUMBUS 49",
"COLUMBUS 50",
"COLUMBUS 51",
"COLUMBUS 52",
"COLUMBUS 53",
"COLUMBUS 54",
"COLUMBUS 55",
"COLUMBUS 56",
"COLUMBUS 57",
"COLUMBUS 58",
"COLUMBUS 59",
"COLUMBUS 60",
"COLUMBUS 61",
"COLUMBUS 62",
"COLUMBUS 63",
"COLUMBUS 64",
"COLUMBUS 65",
"COLUMBUS 66",
"COLUMBUS 67",
"COLUMBUS 68",
"COLUMBUS 69",
"COLUMBUS 70",
"COLUMBUS 71",
"COLUMBUS 72",
"COLUMBUS 73",
"COLUMBUS 74",
"COLUMBUS 75",
"COLUMBUS 76",
"COLUMBUS 77",
"COLUMBUS 78",
"COLUMBUS 79",
"COLUMBUS 80",
"COLUMBUS 81",
"COLUMBUS 82",
"COLUMBUS 83",
"COLUMBUS 84",
"COLUMBUS 85",
"COLUMBUS 86",
"COLUMBUS 87",
"DUBLIN 01",
"DUBLIN 02",
"DUBLIN 03",
"DUBLIN 04",
"FRANKLIN",
"GAHANNA 01",
"GAHANNA 02",
"GAHANNA 03",
"GAHANNA 04",
"GRANDVIEW",
"GROVE CITY 01",
"GROVE CITY 02",
"GROVE CITY 03",
"GROVE CITY 04",
"GROVEPORT",
"HAMILTON",
"HILLIARD 01",
"HILLIARD 02",
"HILLIARD 03",
"HILLIARD 04",
"JACKSON",
"JEFFERSON",
"MADISON",
"MARBLE CLIFF",
"MIFFLIN",
"MINERVA PARK",
"NEW ALBANY",
"NORWICH",
"OBETZ",
"PERRY",
"PLAIN",
"PLEASANT",
"PRAIRIE",
"REYNOLDSBURG 01",
"REYNOLDSBURG 02",
"REYNOLDSBURG 03",
"REYNOLDSBURG 04",
"RIVERLEA",
"SHARON",
"TRURO",
"UPPER ARLINGTON 01",
"UPPER ARLINGTON 02",
"UPPER ARLINGTON 03",
"UPPER ARLINGTON 04",
"UPPER ARLINGTON 05",
"UPPER ARLINGTON 06",
"URBANCREST",
"VALLEYVIEW",
"WASHINGTON",
"WESTERVILLE 01",
"WESTERVILLE 02",
"WESTERVILLE 03",
"WESTERVILLE 04",
"WESTERVILLE 05",
"WHITEHALL 01",
"WHITEHALL 02",
"WHITEHALL 03",
"WHITEHALL 04",
"WORTHINGTON 01",
"WORTHINGTON 02",
"WORTHINGTON 03",
"WORTHINGTON 04"]

def create_record(line, COL_LABELS):
    
    def get(col_name):
        return line[COL_LABELS.index(col_name)]

    record = {
        'name': f'{get("LASTNAME")}, {get("FIRSTNAME")} ' + \
            f'{get("MIDDLE")} {get("SUFFIX")}',
        'house-number': get("RES_HOUSE"),
        'house-fraction': get("RES_FRAC"),
        'street': get("RES STREET"),
        'apt': get("RES_APT"),
    }
    return record

def process(file_name, output_dir):
    ward_lists = {}
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        COL_LABELS = next(reader)
        filtered = (line for line in reader if 'D' in line[COL_LABELS.index('PARTY')])
        for line in filtered:
            assert(len(line) == len(COL_LABELS))
            ward = line[COL_LABELS.index('PRECINCT_NAME_WITH_SPLIT')]
            ward = ward.split('-')[0]
            ward = ward.strip()
            record = create_record(line, COL_LABELS)
            ward_lists.setdefault(ward, []).append(record)
    for ward in ward_lists:
        ward_lists[ward].sort(key=lambda rec: (rec['street'], int(rec['house-number']) % 2, int(rec['house-number']), rec['house-fraction'], rec['apt']))
        output = [ward]
        for record in ward_lists[ward]:
            apt = record['apt'].strip()
            if apt:
                apt = 'APT ' + apt.replace('APT', '')
            output.append(
f"{record['house-number']}\
\t{record['house-fraction']}\
\t{record['street']}\
\t{apt}\
\t{record['name']}")
        output = '\n'.join(output)
        with open(f'{output_dir}/' + ward.replace(' ', '-') + '.csv', 'w') as f:
            f.write(output)



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('''Takes two arguments:
1. The voterfile to read
2. The directory for output files''')
        quit()
    input_file, output_dir = sys.argv[1], sys.argv[2]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    process(input_file, output_dir)
