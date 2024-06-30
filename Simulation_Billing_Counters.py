import heapq
import numpy as np

class Simulation:
    def __init__(self, arrival_rate, num_counters, mean_service_time, service_time_variance, num_customers):
        self.arrival_rate = arrival_rate
        self.num_counters = num_counters
        self.mean_service_time = mean_service_time
        self.service_time_variance = service_time_variance
        self.num_customers = num_customers
        self.global_clock = 0
        self.total_waiting_time = 0

        # Initialize heaps
        self.queue_heap = [(0, 0) for _ in range(num_counters)]  # (number of customers, next free time)
        heapq.heapify(self.queue_heap)
        self.event_heap = []  # (departure time, queue index, arrival time, departure time)

        # Generate customer arrival times based on a fixed rate λ
        self.arrival_times = np.arange(1, num_customers + 1) / arrival_rate
        self.current_customer = 0

    def generate_service_time(self):
        return np.random.normal(self.mean_service_time, self.service_time_variance)

    def run_simulation(self):
        while self.current_customer < self.num_customers or self.event_heap:
            if self.current_customer < self.num_customers and (not self.event_heap or self.arrival_times[self.current_customer] < self.event_heap[0][0]):
                self.process_arrival()
            else:
                self.process_departure()

        return self.total_waiting_time / self.num_customers

    def process_arrival(self):
        arrival_time = self.arrival_times[self.current_customer]
        self.global_clock = arrival_time

        # Find the queue with the smallest length
        num_customers, next_free_time = heapq.heappop(self.queue_heap)
        service_time = self.generate_service_time()
        start_service_time = max(arrival_time, next_free_time)
        departure_time = start_service_time + service_time

        # Calculate waiting time for the customer
        waiting_time = start_service_time - arrival_time

        # Print arrival, departure, and waiting times
        print(f"Customer {self.current_customer + 1}: Arrival at {arrival_time:.2f}, Start Service at {start_service_time:.2f}, Departure at {departure_time:.2f}, Waiting Time: {waiting_time:.2f}")

        # Update total waiting time
        self.total_waiting_time += waiting_time

        # Update the queue heap and event heap
        heapq.heappush(self.queue_heap, (num_customers + 1, departure_time))
        heapq.heappush(self.event_heap, (departure_time, self.current_customer, arrival_time, departure_time))

        self.current_customer += 1

    def process_departure(self):
        departure_time, queue_index, arrival_time, _ = heapq.heappop(self.event_heap)
        self.global_clock = departure_time

        # Find the queue to update in the queue heap
        for i in range(len(self.queue_heap)):
            if self.queue_heap[i][1] == departure_time:
                num_customers, next_free_time = self.queue_heap[i]
                self.queue_heap[i] = (num_customers - 1, next_free_time)
                heapq.heapify(self.queue_heap)
                break

arrival_rate = 3 
num_counters = 2 
mean_service_time = 2.0  
service_time_variance = 0.5  
num_customers = 10 


'''arrival_rate = float(input("Enter arrival rate (R): "))
num_counters = int(input("Enter number of billing counters (k): "))
mean_service_time = float(input("Enter mean service time (µ): "))
service_time_variance = float(input("Enter service time variance (σ): "))
num_customers = int(input("Enter number of customers (N): "))'''

sim = Simulation(arrival_rate, num_counters, mean_service_time, service_time_variance, num_customers)
average_waiting_time = sim.run_simulation()

print(f"Average waiting time: {average_waiting_time}")