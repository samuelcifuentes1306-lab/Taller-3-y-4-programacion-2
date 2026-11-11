def linea_a_fila(linea):
    fila = []
    for caracter in linea:
        fila.append(int(caracter))
    return fila


def fila_a_texto(fila):
    texto = ""
    for numero in fila:
        texto = texto + str(numero)
    return texto


def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num:
            return False
        if tablero[i][col] == num:
            return False
    inicio_fila = (fila // 3) * 3
    inicio_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_col + j] == num:
                return False
    return True


def buscar_vacia(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return [i, j]
    return [-1, -1]


def resolver(tablero):
    posicion = buscar_vacia(tablero)
    fila = posicion[0]
    col = posicion[1]
    if fila == -1:
        return True
    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            if resolver(tablero):
                return True
            tablero[fila][col] = 0
    return False


casos = int(input())
for caso in range(casos):
    tablero = []
    for i in range(9):
        tablero.append(linea_a_fila(input()))
    resolver(tablero)
    for fila in tablero:
        print(fila_a_texto(fila))