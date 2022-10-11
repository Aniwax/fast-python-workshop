# first line: 1
@memory_disk.cache
def fibonacci_disk(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci_disk(n - 1) + fibonacci_disk(n - 2)
