import heapq


class Passenger:

    def __init__(self, passenger_id, has_preboarding=False, delayed_at_control=False):
        self.passenger_id = passenger_id
        self.has_preboarding = has_preboarding
        self.delayed_at_control = delayed_at_control

        if has_preboarding:
            self.priority = 0
        elif delayed_at_control:
            self.priority = 2
        else:
            self.priority = 1

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.passenger_id < other.passenger_id

    def __repr__(self):
        status = "PREBOARDING" if self.has_preboarding else ("DELAYED" if self.delayed_at_control else "NORMAL")
        return f"Passenger(id={self.passenger_id}, {status})"


class AirportBoardingQueue:

    def __init__(self, total_passengers, preboarding_count):
        self.X = total_passengers
        self.Y = preboarding_count
        self.regular_count = self.X - self.Y
        self.priority_queue = []
        self.boarding_order = []
        self.passengers = []

        self._generate_passengers()
        self._build_priority_queue()

    def _generate_passengers(self):
        for i in range(1, self.Y + 1):
            self.passengers.append(Passenger(i, has_preboarding=True))

        regular_id = self.Y + 1
        regular_counter = 0
        for i in range(self.regular_count):
            regular_counter += 1
            is_delayed = (regular_counter % 10 == 0)
            self.passengers.append(Passenger(regular_id, delayed_at_control=is_delayed))
            regular_id += 1

    def _build_priority_queue(self):
        for passenger in self.passengers:
            heapq.heappush(self.priority_queue, passenger)

    def process_boarding(self):
        queue_copy = list(self.priority_queue)
        heapq.heapify(queue_copy)

        self.boarding_order = []
        boarding_position = 0

        while queue_copy:
            passenger = heapq.heappop(queue_copy)
            boarding_position += 1
            effective_time = 3 if passenger.delayed_at_control else 1
            self.boarding_order.append({
                'position': boarding_position,
                'passenger': passenger,
                'effective_time': effective_time
            })

        return self.boarding_order

    def find_33rd_regular_passenger(self):
        if not self.boarding_order:
            self.process_boarding()

        regular_boarded = 0
        for entry in self.boarding_order:
            if not entry['passenger'].has_preboarding:
                regular_boarded += 1
                if regular_boarded == 33:
                    return entry
        return None

    def find_kth_delayed_passenger(self, k=1):
        if not self.boarding_order:
            self.process_boarding()

        delayed_count = 0
        for entry in self.boarding_order:
            if entry['passenger'].delayed_at_control:
                delayed_count += 1
                if delayed_count == k:
                    return entry
        return None

    def get_boarding_order(self):
        if not self.boarding_order:
            self.process_boarding()
        return self.boarding_order

    def print_summary(self):
        if not self.boarding_order:
            self.process_boarding()

        print("=" * 70)
        print("BOARDING SIMULATION")
        print(f"Total passengers (X): {self.X}")
        print(f"Preboarding (Y): {self.Y}")
        print(f"Regular (X-Y): {self.regular_count}")
        delayed_total = sum(1 for p in self.passengers if p.delayed_at_control)
        print(f"Delayed at control (every 10th of X-Y): {delayed_total}")
        print("=" * 70)

        result_33 = self.find_33rd_regular_passenger()
        if result_33:
            print(f"\n[Q1] The 33rd regular passenger (from X-Y set) who boarded:")
            print(f"  -> Boarding position: {result_33['position']}")
            print(f"  -> {result_33['passenger']}")
        else:
            print("\n[Q1] Not enough regular passengers to reach 33.")

        for k in [1, 2, 3]:
            result_k = self.find_kth_delayed_passenger(k)
            if result_k:
                print(f"\n[Q2] The {k}-th delayed passenger (every 10th):")
                print(f"  -> Boarding position: {result_k['position']}")
                print(f"  -> {result_k['passenger']}")
                print(f"  -> Effective time: {result_k['effective_time']}x")

        print(f"\n[Q3] Full boarding order:")
        print("-" * 60)
        print(f"{'Pos.':<6} {'ID':<6} {'Type':<15} {'Eff. time':<10}")
        print("-" * 60)
        for entry in self.boarding_order:
            p = entry['passenger']
            ptype = "PREBOARDING" if p.has_preboarding else ("DELAYED" if p.delayed_at_control else "NORMAL")
            print(f"{entry['position']:<6} {p.passenger_id:<6} {ptype:<15} {entry['effective_time']:<10}")


if __name__ == "__main__":
    X = 100
    Y = 20

    airport = AirportBoardingQueue(X, Y)
    airport.print_summary()