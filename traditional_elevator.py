import random

T = 0
DWELL_TIME = 10
CALLS = []
TOTAL_DISTANCE = 0

CURRENT_FLOOR = 1
DIRECTION = "idle"
UP_CALLS = set()
DOWN_CALLS = set()
DESTINATIONS = set()
WAITING_DESTINATIONS = {}


def generate_passengers(n, seed):
    random.seed(seed)
    passengers = []

    for _ in range(n):
        passengers.append(
            {
                "call_time": random.randint(1, 600),
                "origin": random.randint(1, 10),
                "destination": random.randint(1, 10),
            }
        )

    return passengers


def determine_direction():
    has_call_above = any(floor > CURRENT_FLOOR for floor in UP_CALLS)
    has_destinations_above = any(floor > CURRENT_FLOOR for floor in DESTINATIONS)
    has_call_below = any(floor < CURRENT_FLOOR for floor in DOWN_CALLS)
    has_destinations_below = any(floor < CURRENT_FLOOR for floor in DESTINATIONS)

    if DIRECTION == "up":
        if has_call_above or has_destinations_above:
            return "up"
        elif DOWN_CALLS or has_destinations_below:
            return "down"
        else:
            return "idle"
    elif DIRECTION == "down":
        if has_call_below or has_destinations_below:
            return "down"
        elif UP_CALLS or has_destinations_above:
            return "up"
        else:
            return "idle"
    else:
        if UP_CALLS or has_destinations_above:
            return "up"
        elif DOWN_CALLS or has_destinations_below:
            return "down"
        else:
            return "idle"


PASSENGERS = generate_passengers(10, 1234)
elevator_busy_until = 0

# 10 minutes, 10 floors
# up/down_calls = floors from which a call to go up/down has come from
# waiting_destinations = O-D pairs which elevator will see after "picking up" the passenger
print(PASSENGERS)
while T < 600:
    for passenger in PASSENGERS:
        # new call is received
        if passenger.get("call_time") == T:
            origin = passenger.get("origin")
            destination = passenger.get("destination")
            UP_CALLS.add(origin) if destination > origin else DOWN_CALLS.add(origin)
            if origin not in WAITING_DESTINATIONS:
                WAITING_DESTINATIONS[origin] = []
            WAITING_DESTINATIONS[origin].append(destination)

    if T >= elevator_busy_until:
        # elevator is stopping
        if CURRENT_FLOOR in (DESTINATIONS | UP_CALLS | DOWN_CALLS):
            print(f"T={T}: Stopping at floor {CURRENT_FLOOR} - Pickups/Dropoffs")
            # dropping someone(s) off here
            if CURRENT_FLOOR in DESTINATIONS:
                DESTINATIONS.remove(CURRENT_FLOOR)

            # picking up someone(s)
            if CURRENT_FLOOR in UP_CALLS or CURRENT_FLOOR in DOWN_CALLS:
                if CURRENT_FLOOR in WAITING_DESTINATIONS:
                    for dest in WAITING_DESTINATIONS[CURRENT_FLOOR]:
                        DESTINATIONS.add(dest)
                    del WAITING_DESTINATIONS[CURRENT_FLOOR]
                UP_CALLS.discard(CURRENT_FLOOR)
                DOWN_CALLS.discard(CURRENT_FLOOR)

            elevator_busy_until = T + DWELL_TIME
        else:
            old_floor = CURRENT_FLOOR
            DIRECTION = determine_direction()
            if DIRECTION == "up" and CURRENT_FLOOR < 10:
                CURRENT_FLOOR += 1
                TOTAL_DISTANCE += 1
                print(f"T={T}: Moved up from {old_floor} to {CURRENT_FLOOR}")
            elif DIRECTION == "down" and CURRENT_FLOOR > 1:
                CURRENT_FLOOR -= 1
                TOTAL_DISTANCE += 1
                print(f"T={T}: Moved down from {old_floor} to {CURRENT_FLOOR}")
            elif DIRECTION == "idle":
                print(f"T={T}: Idle at floor {CURRENT_FLOOR}")
    T += 1
