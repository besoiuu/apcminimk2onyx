# bank_manager.py

# Variabila globală pentru banca curentă
MAX_BANCI = 8
banca_curenta = 0

def increment_bank():
    """
    Crește banca curentă cu 1, resetând-o la 0 dacă depășește MAX_BANCI.
    """
    global banca_curenta
    if banca_curenta < MAX_BANCI - 1:
        banca_curenta += 1
    else:
        banca_curenta = 0
    print(f'📦 Banca curentă: {banca_curenta}')

def decrement_bank():
    """
    Scade banca curentă cu 1, resetând-o la MAX_BANCI - 1 dacă ajunge la 0.
    """
    global banca_curenta
    if banca_curenta > 0:
        banca_curenta -= 1
    else:
        banca_curenta = MAX_BANCI - 1
    print(f'📦 Banca curentă: {banca_curenta}')

def get_banca_curenta():
    """
    Returnează banca curentă.
    """
    return banca_curenta
