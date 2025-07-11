banca_curenta = 0
MAX_BANCI = 8

def increment_bank():
    global banca_curenta
    if banca_curenta < MAX_BANCI - 1:
        banca_curenta += 1
    else:
        banca_curenta = 0
    print(f'📦 Banca curentă: {banca_curenta}')

def decrement_bank():
    global banca_curenta
    if banca_curenta > 0:
        banca_curenta -= 1
    else:
        banca_curenta = MAX_BANCI - 1
    print(f'📦 Banca curentă: {banca_curenta}')
