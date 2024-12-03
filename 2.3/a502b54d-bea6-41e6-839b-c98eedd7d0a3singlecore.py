import time

def factorize(numbers):
    start_time = time.time()
    result = set()
    for num in numbers:
        factors = {i for i in range(1, num + 1) if num % i == 0}
        result.update(factors)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 4)
    print(f"Czas wykonania: {elapsed_time} sekundy")
    return list(result)


numbers_to_factorize = [12441111, 18444333, 282111, 3511, 425555, 5555, 7773, 3113, 8131]
result = factorize(numbers_to_factorize)

print("Lista unikalnych liczb przez które liczby są podzielne:")
print(result)
