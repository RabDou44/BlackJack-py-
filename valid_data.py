def int_input(in_str, upper=8, lower=0):
    num = 0
    while True:
        try:
            num = int(input(in_str))
        except ValueError:
            continue
        except TypeError:
            continue
        else:
            if lower <= num <= upper:
                break
            print("Must choose between ", lower, "and", upper, ":")
    return num


def float_input(in_str, upper=10000., lower=0.):
    num = 0.
    while True:
        try:
            num = float(input(in_str))
        except ValueError:
            continue
        except TypeError:
            continue
        else:
            if lower <= num <= upper:
                break
            print("Choose value between", lower, upper, "You typed",num)
    return num


def str_input(in_str, upper):
    ans = ''
    while True:
        try:
            ans = input(in_str)
        except ValueError:
            continue
        except TypeError:
            continue
        else:
            if len(ans) > upper:
                print("string must have max %d characters" % upper)
                continue
            else:
                break
    return ans


def yn_input(in_str):
    ans = ''
    while True:
        try:
            ans = input(in_str)
        except ValueError:
            continue
        except TypeError:
            continue
        else:
            if ans == 'y' or ans == 'n':
                break
    return ans

