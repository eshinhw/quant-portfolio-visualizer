def power2iter(m,n):
    
    x = 1
    y = 2 * n
    
    print("Before the loop: x = {}, y = {}".format(x,y))
    
    while (y <= m):
        y = 2 * y
        x = 2 * x
        
        print("Inside the loop: x = {}, y = {}".format(x,y))
    
    return x

print("Returned x = {}".format(power2iter(10,2)))


def longDivision(x,y):
    
    if x == 0:
        return (0,0)
    else:
        (q,r) = longDivision(x//2,y)
        
        if 2 * r + (x % 2) < y:
            return (2 * q, 2 * r + (x % 2))
        else:
            return (2 * q + 1, 2 * r + (x % 2) - y)

print(longDivision(10,3))