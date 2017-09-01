import random

# seq = [2, 6, 4, 3, 1, 7, 9, 8, 5]


def generate():
    return [(random.randint(0, 100), 1) for x in range(0, 10)]


def find_top_k(a, k):
    return find(a, k, 0, len(a) - 1)


def find(a, k, p, r):
    print("FIND:", a, k, p, r)
    if k <= 0:
        return []
    else:
        q = partition(a, p, r)
        if q - p <= k:
            return a[p:q] + find(a, k - (q - p), q, r)
        else:
            return find(a, k, p, q - 1)


def partition(a, p, r):
    x = a[r][0]
    i = p - 1
    for j in range(p, r):
        if a[j][0] <= x:
            i += 1
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp
    tmp = a[i + 1]
    a[i + 1] = a[r]
    a[r] = tmp
    return i + 1

print(find_top_k(generate(), 4))

# print(random.)



