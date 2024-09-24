from TCP import Mensaje_TCP

def false_arr(n):
    arr = []
    for i in range(n):
        arr += [False]
    return arr

def check_arr(array):
    for j in range(len(array)):
        if array[j] == False:
            return False
    return True

a = false_arr(5)
b = [True, True, True, False]
c = [True, True, True]

print(check_arr(a))
print(check_arr(b))
print(check_arr(c))