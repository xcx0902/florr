import pymem.exception
from pymem import Pymem
import psutil

petal_ids = {'Basic': 1, 'Light': 2, 'Rock': 3, 'Square': 4, 'Rose': 5, 'Stinger': 6, 'Iris': 7, 'Wing': 8, 'Missile': 9, 'Grapes': 10, 'Cactus': 11, 'Faster': 12, 'Bubble': 13, 'Pollen': 14, 'Dandelion': 15, 'Egg': 16, 'Antennae': 17, 'Heavy': 18, 'YinYang': 19, 'Web': 20, 'Honey': 21, 'Leaf': 22, 'Salt': 23, 'Rice': 24, 'Corn': 25, 'Sand': 26, 'Pincer': 27, 'Yucca': 28, 'Magnet': 29, 'Yggdrasil': 30, 'Starfish': 31, 'Pearl': 32, 'Lightning': 33, 'Jelly': 34, 'Claw': 35, 'Shell': 36, 'Cutter': 37, 'Dahlia': 38, 'Uranium': 39, 'Sponge': 40, 'Soil': 41, 'Fangs': 42, 'ThirdEye': 43, 'Peas': 44, 'Stick': 45, 'Clover': 46, 'Powder': 47, 'Air': 48, 'Basil': 49, 'Orange': 50}

petal_levels = {'Common': 1, 'Unusual': 2, 'Rare': 3, 'Epic': 4, 'Legendary': 5, 'Mythic': 6, 'Ultra': 7, 'Super': 8}

browser_name = 'edge.exe'

def get_create_time(p: psutil.Process):
    return p.create_time()

def get_pid(p: psutil.Process):
    return p.pid

def find_process(name):
    res = []
    pids = psutil.pids()
    for pid in pids:
        if psutil.pid_exists(pid):
            p = psutil.Process(pid)
            s = p.name()
            if s.find(name) != -1:
                res.append(p)
                # print(pid, p.create_time())
                # print(pid, p.name())
    
    res.sort(key=get_create_time, reverse=True)
    res = list(map(get_pid, res))
    return res

def check_florr(pm: Pymem):
    if not pm:
        return False
    if pm.pattern_scan_all(b'This pretty little flower is called...'):
        return True
    return False

def find_florr_pid(browser_name):
    print('Start finding florr process...')
    l = find_process(browser_name)
    pid = 0
    pm = None
    for each in l:
        pid = each
        print('Checking pid=%d' % pid)
        try:
            pm = Pymem(pid)
        except pymem.exception.CouldNotOpenProcess:
            continue
        if check_florr(pm):
            print('florr pid=%d' % pid)
            return pid
    return None

def number2bytes(num):
    res = []
    for i in range(4):
        res.append(num % 256)
        num //= 256
    return bytes(res)

def fuck_re(pat: bytes):
    rech = [b'\\', b'*', b'.', b'?', b'+', b'$', b'^', b'[', b']', b'(', b')', b'{', b'}', b'|', b'/']
    for each in rech:
        pat = pat.replace(each, b'\\' + each)
    return pat

# pid = find_florr_pid(browser_name)
# pm = Pymem(pid)

def scan_inventory_base(pid: int, inventory: list):
    global petal_ids
    """
    -1: Unknown petal name
    -2: Cannot Find
    """
    pm = Pymem(pid)
    qry = {}
    for l in inventory:
        petal_name = l[0]
        if petal_name not in petal_ids:
            return -1
        l = l[1:]
        inv = bytes()
        for i in range(8):
            if i < len(l):
                inv += (number2bytes(int(l[i])))
            else:
                inv += (number2bytes(0))
        qry[petal_ids[petal_name]] = fuck_re(inv)

    empty = b'.' * 4 * 8
    queryed = bytes()
    for petal_name in petal_ids:
        petal_id = petal_ids[petal_name]
        if petal_id in qry: ## BUG!
            queryed += qry[petal_id]
        else:
            queryed += empty
    queryed = queryed.rstrip(b'.')
    tmp = queryed.lstrip(b'.')
    delta = len(queryed) - len(tmp)
    queryed = tmp
    resp = pm.pattern_scan_all(queryed, return_multiple=True)
    if len(resp) == 0:
        return -2
    base = resp[-1] - delta
    return base


### Inventory Enter & Scan

# print('Enter Inventory:')

# inp = input()

# inventory = {}

# while inp != '':
#     l = inp.split(' ')
#     petal_name = l[0]
#     if petal_name not in petal_ids:
#         print('Wrong Name!')
#         inp = input()
#         continue
#     l = list(map(int, l[1:]))
#     inv = bytes()
#     for i in range(7):
#         if i < len(l):
#             inv += (number2bytes(int(l[i])))
#         else:
#             inv += (number2bytes(0))
#     inventory[petal_ids[petal_name]] = fuck_re(inv)
#     inp = input()

# # print(inventory)

# empty = b'.' * 4 * 7

# queryed = bytes()

# for petal_name in petal_ids:
#     petal_id = petal_ids[petal_name]
#     if petal_id in inventory:
#         queryed += inventory[petal_id]
#     else:
#         queryed += empty

# queryed = queryed.rstrip(b'.')
# tmp = queryed.lstrip(b'.')
# delta = len(queryed) - len(tmp)
# queryed = tmp

# print(queryed)

# print('Scanning Inventory Base Address...')

# base = pm.pattern_scan_all(queryed, return_multiple=True)[-1] - delta

# print('Inventory Base Address=%d' % base)


### Modify

def modify_inventory(pid: int, base_addr: int, petal_name: str, petal_level: str, num: int):
    pm = Pymem(pid)
    if petal_name not in petal_ids:
        return -1
    petal_id = petal_ids[petal_name]
    petal_level = petal_levels[petal_level]
    pm.write_int(base_addr + (petal_id - 1) * 4 * 8 + (petal_level - 1) * 4, num)
    return 0


# print('Enter Modification:')

# inp = input()

# while inp != '':
#     petal_name, petal_level, num = inp.split(' ')
#     num = int(num)
#     petal_id = petal_ids[petal_name]
#     petal_level = petal_levels[petal_level]
#     pm.write_int(base + (petal_id - 1) * 4 * 7 + (petal_level - 1) * 4, num)
#     inp = input()
