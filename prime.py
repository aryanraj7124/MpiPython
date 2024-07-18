# from mpi4py import MPI
# import numpy as np
# import math

# def initialize_sieve(start, end):
#     return np.ones(end - start + 1, dtype=bool)

# def segmented_sieve(start, end, is_prime):
#     range_size = end - start + 1
#     small_primes_size = int(math.sqrt(end)) + 1
#     small_primes = []

#     # Small prime sieve
#     is_small_prime = np.ones(small_primes_size + 1, dtype=bool)
#     is_small_prime[0:2] = False

#     for i in range(2, int(math.sqrt(small_primes_size)) + 1):
#         if is_small_prime[i]:
#             for j in range(i * i, small_primes_size + 1, i):
#                 is_small_prime[j] = False

#     # Collect small primes
#     for i in range(2, small_primes_size + 1):
#         if is_small_prime[i]:
#             small_primes.append(i)

#     # Apply small primes to the large range
#     for prime in small_primes:
#         start_index = max(prime * prime, start + (prime - start % prime) % prime)
#         for j in range(start_index, end + 1, prime):
#             is_prime[j - start] = False

# def find_primes_in_range(start, end):
#     is_prime = initialize_sieve(start, end)
#     segmented_sieve(start, end, is_prime)
#     primes = [num for num in range(start, end + 1) if is_prime[num - start]]
#     return primes

# if __name__ == "__main__":
#     target_prime_index = 100000000 # Example: 1 millionth prime
#     comm = MPI.COMM_WORLD
#     rank = comm.Get_rank()
#     size = comm.Get_size()

#     start = 2
#     range_size = 1000000  # Initial range size

#     found = False
#     global_prime_list = []

#     while not found:
#         local_start = start + rank * range_size
#         local_end = local_start + range_size - 1

#         # Each process finds primes in its range
#         local_primes = find_primes_in_range(local_start, local_end)

#         # Gather primes from all processes at root
#         all_primes = comm.gather(local_primes, root=0)

#         if rank == 0:
#             # Flatten the list of primes
#             flat_primes = [prime for sublist in all_primes for prime in sublist]
#             global_prime_list.extend(flat_primes)

#             if len(global_prime_list) >= target_prime_index:
#                 global_prime_list.sort()
#                 nth_prime = global_prime_list[target_prime_index - 1]
#                 found = True
#             else:
#                 start += range_size * size  # Increase the range for the next iteration

#         found = comm.bcast(found, root=0)

#     if rank == 0 and found:
#         print(f"The {target_prime_index}th prime number is {nth_prime}")


from mpi4py import MPI
import numpy as np
import math
import time

def initialize_sieve(start, end):
    return np.ones(end - start + 1, dtype=bool)

def segmented_sieve(start, end, is_prime):
    range_size = end - start + 1
    small_primes_size = int(math.sqrt(end)) + 1
    small_primes = []

    # Small prime sieve
    is_small_prime = np.ones(small_primes_size + 1, dtype=bool)
    is_small_prime[0:2] = False

    for i in range(2, int(math.sqrt(small_primes_size)) + 1):
        if is_small_prime[i]:
            for j in range(i * i, small_primes_size + 1, i):
                is_small_prime[j] = False

    # Collect small primes
    for i in range(2, small_primes_size + 1):
        if is_small_prime[i]:
            small_primes.append(i)

    # Apply small primes to the large range
    for prime in small_primes:
        start_index = max(prime * prime, start + (prime - start % prime) % prime)
        for j in range(start_index, end + 1, prime):
            is_prime[j - start] = False

def find_primes_in_range(start, end):
    is_prime = initialize_sieve(start, end)
    segmented_sieve(start, end, is_prime)
    primes = [num for num in range(start, end + 1) if is_prime[num - start]]
    return primes

if __name__ == "__main__":
    target_prime_index = 200000 # Example: 100 millionth prime
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start_time = time.time()

    start = 2
    range_size = 10000000  # Initial range size

    found = False
    global_prime_list = []

    while not found:
        local_start = start + rank * range_size
        local_end = local_start + range_size - 1

        # Each process finds primes in its range
        local_primes = find_primes_in_range(local_start, local_end)

        # Gather primes from all processes at root
        all_primes = comm.gather(local_primes, root=0)

        if rank == 0:
            # Flatten the list of primes
            flat_primes = [prime for sublist in all_primes for prime in sublist]
            global_prime_list.extend(flat_primes)

            if len(global_prime_list) >= target_prime_index:
                global_prime_list.sort()
                nth_prime = global_prime_list[target_prime_index - 1]
                found = True
            else:
                start += range_size * size  # Increase the range for the next iteration

        found = comm.bcast(found, root=0)

    end_time = time.time()

    if rank == 0 and found:
        print(f"The {target_prime_index}th prime number is {nth_prime}")
        print(f"Time taken: {end_time - start_time} seconds")
