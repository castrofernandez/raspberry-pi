def queHoraEs(h):
    if h > 12:
        h -= 12
    if h == 1:
        return "Es la una"
    elif h == 2:
        return "Son las dos"
    elif h == 3:
        return "Son las tres"
    elif h == 4:
        return "Son las cuatro"
    elif h == 5:
        return "Son las cinco"
    elif h == 6:
        return "Son las seis"
    elif h == 7:
        return "Son las siete"
    elif h == 8:
        return "Son las ocho"
    elif h == 9:
        return "Son las nueve"
    elif h == 10:
        return "Son las diez"
    elif h == 11:
        return "Son las once"
    else:
        return "Son las doce"