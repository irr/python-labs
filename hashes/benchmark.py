import mmh3
import cityhash
import timeit
from datetime import datetime

input_string = "example_string_to_test_the_performance_of_hash_functions"

def test_murmurhash():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Year, month, day, hour, minute, second, microsecond

    hash_value = mmh3.hash128(input_string, signed=False)

    sortable_hash = f"{timestamp}-{hash_value:032x}"
    
    return sortable_hash

def test_cityhash():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Year, month, day, hour, minute, second, microsecond
    
    hash_value = cityhash.CityHash128(input_string)
    
    sortable_hash = f"{timestamp}-{hash_value:032x}"
    
    return sortable_hash

murmurhash_time = timeit.timeit(test_murmurhash, number=100000)
print(f"MurmurHash execution time for 100,000 iterations: {murmurhash_time:.6f} seconds")

cityhash_time = timeit.timeit(test_cityhash, number=100000)
print(f"CityHash execution time for 100,000 iterations: {cityhash_time:.6f} seconds")

print(f"Sortable CityHash example: {test_cityhash()}")
print(f"Sortable MurmurHash example: {test_murmurhash()}")

if murmurhash_time < cityhash_time:
    faster_percentage = ((cityhash_time - murmurhash_time) / cityhash_time) * 100
    print(f"MurmurHash is faster by approximately {faster_percentage:.2f}%")
else:
    faster_percentage = ((murmurhash_time - cityhash_time) / murmurhash_time) * 100
    print(f"CityHash is faster by approximately {faster_percentage:.2f}%")
