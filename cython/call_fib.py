import primes
import primes_py
from time import time
start = time()
for _ in range(100):
    primes.primes(1000)
one = time() - start
print one
start2 = time()
for __ in range(100):
    primes_py.primes(1000)
two = time() - start2
print two
print
print two/one
