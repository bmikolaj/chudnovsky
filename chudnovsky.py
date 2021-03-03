import decimal
from mpmath import mp
import sys



# Calculates factorial using loop instead of recursion to avoid stack limit
def fact(n):
    if n == 0:
        return 1
    else:
        res = 1
        for i in range(1,n+1):
            res = res*i

        return res

# Keeps a running list of previously calculated denominators
den_list = []

# Denominator- Calculates the sum from 0 to k.
def den(k_large):
    result = 0
    for k in range(0,k_large+1):
        # If k exists in the denominator list, retrieve that result instead of calculating
        if len(den_list) > 0 and len(den_list) > k:
            result+=den_list[k]
        else: # calculate
            a = decimal.Decimal(fact(6*k)*(545140134*k+13591409))
            b = decimal.Decimal(fact(3*k)*(fact(k)**3)*((-262537412640768000)**k))
            res = a / b
            result+=res
            if len(den_list) == k: # Store result in den_list
                den_list.append(res)

    return result

# Numerator- root_precision is the number of significant digits to use when calculating the root.
def num(root_precision):
    p = decimal.getcontext().prec
    decimal.getcontext().prec = root_precision
    d = decimal.Decimal(10005).sqrt()
    decimal.getcontext().prec = p
    #print(d)
    return 426880 * decimal.Decimal(10005).sqrt()
    

# Calculates the Chudnovsky Algorithm for a given k, and precision.
def chudnovsky(k, root_precision):
    return num(root_precision)/den(k)

# Returns which digit of pi is errant in a using b as a reference
def digit_compare(a, b):
    a = str(a)
    b = str(b)

    digit = 0
    for i,d in enumerate(a):
        if d == '.':
            continue
        if b[i]==d:
            digit+=1
        else:
            return digit


def main():
    precision = int(sys.argv[1]) # 1st argument sets decimal precision
    mp.dps = precision  # set number of digits of precision for pi
    decimal.getcontext().prec = precision  # set significant figures for decimal numbers
    pi = mp.pi

    k=0
    prev_error = 0
    while True:
        print("k =",k)
        pi_estimate = chudnovsky(k, precision)
        print(pi_estimate)
        error = digit_compare(pi_estimate, pi)
        print('Error: {}th digit'.format(error))

        # a repeating digit that is errant implies the end of precision
        if prev_error == error:
            break
        else: # keep calculating
            k+=1
            prev_error = error


if __name__ == '__main__':
    main()