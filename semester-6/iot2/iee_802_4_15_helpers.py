import math

ELEM = 16
BASE_SD = 960

def get_bo_for_bi(bi):
    bi = bi * 1_000_000
    return round(math.log2(bi / (BASE_SD * ELEM)))

def get_so_for_sd(sd):
    sd *= 1_000_000
    return round(math.log2(sd / (BASE_SD * ELEM)))

if __name__ == '__main__':
    print(get_bo_for_bi(4))
    print(get_so_for_sd(0.25))
