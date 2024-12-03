import time
import multiprocessing

def factorize_helper(num):
    return {i for i in range(1, num + 1) if num % i == 0}

def factorize_parallel(numbers):
    start_time = time.time()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_helper, numbers)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 4)

    print(f"Czas wykonania: {elapsed_time} sekundy")

    unique_factors = set().union(*results)
    return list(unique_factors)

if __name__ == '__main__':
    numbers_to_factorize = [12441111, 18444333, 282111, 3511, 425555, 5555, 7773, 3113, 8131]
    result = factorize_parallel(numbers_to_factorize)

    print("Lista unikalnych liczb przez które liczby są podzielne:")
    print(result)
