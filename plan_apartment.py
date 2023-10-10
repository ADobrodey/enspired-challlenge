#!/usr/bin/env python3
import sys, getopt

HORIZONTAL_WALLS = ['+', '-']
VERTICAL_WALLS = ['|', '/', '\\']
CHAIR_TYPES = ['W', 'P', 'S', 'C']


class Room:
    def __init__(self):
        self.name = ''
        self.name_found = False
        self.area = []
        self.chairs = {
            'W': 0,
            'P': 0,
            'S': 0,
            'C': 0
        }

    def process_name(self, symbol: str) -> None:
        if symbol == '(':
            self.name_found = True
            return
        if symbol == ')':
            self.name_found = False
            return
        if self.name_found:
            self.name = self.name + symbol

    def add_chair(self, symbol: str) -> None:
        # If symbol is not part of the name
        if symbol in CHAIR_TYPES and not self.name_found:
            self.chairs[symbol] += 1

    def num_chairs(self) -> int:
        return sum(self.chairs.values())

    def __str__(self):
        return (
            self.name +
            ':\n' + f"W: {self.chairs['W']}, P: {self.chairs['P']}, S: {self.chairs['S']}, C: {self.chairs['C']}"
        )

    def __repr__(self):
        return self.name


def main(argv):
    rooms_file = 'rooms.txt'

    try:
        opts, args = getopt.getopt(argv, "hi:", ["help=", "rooms="])
    except getopt.GetoptError:
        print('plan_apartment.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--rooms"):
            rooms_file = arg

    with open(rooms_file) as f:
        rooms_txt = f.read()

    rooms = process_rooms(rooms_txt)
    print_outputs(rooms)


def find_room(rooms_list: set[Room], coords: tuple) -> Room:
    for room in rooms_list:
        if (coords[0] - 1, coords[1]) in room.area:
            return room


def process_rooms(rooms_plan: str) -> set[Room]:
    found_rooms = set()
    rows = rooms_plan.splitlines()
    above_rooms = set()

    for row_idx, row in enumerate(rows):
        temp_room = None

        if row_idx == 0:
            # We skip first line
            continue

        # Scan through symbols
        for idx, char in enumerate(row):
            coordinates = (row_idx, idx)
            if char in HORIZONTAL_WALLS:
                # We ignore horizontal walls
                continue

            if char in VERTICAL_WALLS and idx < len(row):
                # New room started
                if temp_room is not None:
                    above_rooms.add(temp_room)
                temp_room = Room()
                continue

            # Found existing room
            if not rows[row_idx - 1][idx] in HORIZONTAL_WALLS:
                # Check above rooms
                room = find_room(above_rooms, coordinates)
                if room is not None:
                    temp_room = room

            if temp_room:
                temp_room.area.append(coordinates)

                # Process found name
                temp_room.process_name(char)

                # Process chairs
                if char in CHAIR_TYPES:
                    temp_room.add_chair(char)

        found_rooms.update(above_rooms)

    return found_rooms


def print_outputs(apartment_rooms: set[Room]) -> None:
    print('total:\n' +
          f"W: {sum(room.chairs['W'] for room in apartment_rooms)}, " +
          f"P: {sum(room.chairs['P'] for room in apartment_rooms)}, " +
          f"S: {sum(room.chairs['S'] for room in apartment_rooms)}, " +
          f"C: {sum(room.chairs['C'] for room in apartment_rooms)}"
          )

    for room in sorted(apartment_rooms, key=lambda room: room.name):
        print(room)


if __name__ == "__main__":
    main(sys.argv[1:])
