import flet as ft
import pokebase as pk


COLORES_TIPO = {
    "normal": "#a8a77a",
    "fire": "#ee8130",
    "water": "#6390f0",
    "electric": "#f7d02c",
    "grass": "#7ac74c",
    "ice": "#96d9d6",
    "fighting": "#c22e28",
    "poison": "#a33ea1",
    "ground": "#e2bf65",
    "flying": "#a98ff3",
    "psychic": "#f95587",
    "bug": "#a6b91a",
    "rock": "#b6a136",
    "ghost": "#735797",
    "dragon": "#6f35fc",
    "dark": "#705746",
    "steel": "#b7b7ce",
    "fairy": "#d685ad"
}

NOMBRES_TIPO = {
    "normal": "Normal",
    "fire": "Fuego",
    "water": "Agua",
    "electric": "Eléctrico",
    "grass": "Planta",
    "ice": "Hielo",
    "fighting": "Lucha",
    "poison": "Veneno",
    "ground": "Tierra",
    "flying": "Volador",
    "psychic": "Psíquico",
    "bug": "Bicho",
    "rock": "Roca",
    "ghost": "Fantasma",
    "dragon": "Dragón",
    "dark": "Siniestro",
    "steel": "Acero",
    "fairy": "Hada"
}

NOMBRES_STATS = {
    "hp": "HP",
    "attack": "Ataque",
    "defense": "Defensa",
    "special-attack": "Ataque Esp.",
    "special-defense": "Defensa Esp.",
    "speed": "Velocidad"
}


def buscar_pokemon(entrada):
    if entrada.isdigit():
        return pk.pokemon(int(entrada))
    return pk.pokemon(entrada.lower())


def obtener_url(numero):
    base = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"
    return base + str(numero) + ".png"


def crear_chip(texto, color):
    return ft.Container(
        content=ft.Text(texto, color="white", size=14),
        bgcolor=color,
        padding=8,
        border_radius=15
    )


def crear_dato(titulo, valor):
    return ft.Container(
        content=ft.Column([
            ft.Text(titulo, size=12, color="#ffcdd2"),
            ft.Text(valor, size=18, color="white")
        ]),
        bgcolor="#8e0000",
        padding=12,
        border_radius=10,
        width=140
    )


def crear_barra(nombre, valor):
    if valor < 50:
        color = "#ef5350"
    elif valor < 90:
        color = "#ffa726"
    else:
        color = "#66bb6a"
    return ft.Row([
        ft.Container(content=ft.Text(nombre, color="white", size=13), width=100),
        ft.Container(content=ft.Text(str(valor), color="white", size=13), width=35),
        ft.Container(width=valor * 1.2, height=12, bgcolor=color, border_radius=6)
    ])


def obtener_chips_tipos(pokemon):
    chips = []
    for t in pokemon.types:
        nombre = t.type.name
        chips.append(crear_chip(NOMBRES_TIPO[nombre], COLORES_TIPO[nombre]))
    return chips


def obtener_chips_habilidades(pokemon):
    chips = []
    for h in pokemon.abilities:
        texto = h.ability.name
        if h.is_hidden:
            texto = texto + " (oculta)"
        chips.append(crear_chip(texto, "#37474f"))
    return chips


def obtener_barras(pokemon):
    barras = []
    for s in pokemon.stats:
        barras.append(crear_barra(NOMBRES_STATS[s.stat.name], s.base_stat))
    return barras


def obtener_datos(pokemon):
    return [
        crear_dato("ALTURA", str(pokemon.height / 10) + " m"),
        crear_dato("PESO", str(pokemon.weight / 10) + " kg"),
        crear_dato("EXPERIENCIA", str(pokemon.base_experience))
    ]


def main(page: ft.Page):
    page.title = "Pokedex"
    page.padding = 20
    page.bgcolor = "#263238"

    estado = [1]

    image = ft.Image(src=obtener_url(1), width=260, height=260)
    numero = ft.Text("#1", size=20, color="#00e676")
    entrada = ft.TextField(
        label="Nombre o número",
        width=210,
        bgcolor="white",
        color="black"
    )
    mensaje = ft.Text("Escribe un nombre o un número del 1 al 1025", size=12, color="white")

    nombre = ft.Text("", size=32, color="white")
    tipos = ft.Row([])
    estadisticas = ft.Column([])
    datos = ft.Row([])
    habilidades = ft.Row([])

    def mostrar(pokemon):
        estado[0] = pokemon.id
        image.src = obtener_url(pokemon.id)
        numero.value = "#" + str(pokemon.id)
        nombre.value = pokemon.name.upper()
        tipos.controls = obtener_chips_tipos(pokemon)
        estadisticas.controls = obtener_barras(pokemon)
        datos.controls = obtener_datos(pokemon)
        habilidades.controls = obtener_chips_habilidades(pokemon)
        page.update()
        return pokemon.name

    def anterior(e):
        if estado[0] > 1:
            mostrar(pk.pokemon(estado[0] - 1))

    def siguiente(e):
        if estado[0] < 1025:
            mostrar(pk.pokemon(estado[0] + 1))

    def buscar(e):
        texto = entrada.value
        if texto == "":
            mensaje.value = "Escribe algo para buscar"
            page.update()
        elif texto.isdigit() and (int(texto) < 1 or int(texto) > 1025):
            mensaje.value = "El número debe estar entre 1 y 1025"
            page.update()
        else:
            mensaje.value = "Escribe un nombre o un número del 1 al 1025"
            mostrar(buscar_pokemon(texto))

    luces = ft.Row([
        ft.Container(width=50, height=50, bgcolor="#2196f3", border_radius=25),
        ft.Container(width=14, height=14, bgcolor="#ef5350", border_radius=7),
        ft.Container(width=14, height=14, bgcolor="#ffee58", border_radius=7),
        ft.Container(width=14, height=14, bgcolor="#66bb6a", border_radius=7)
    ])

    pantalla = ft.Container(
        content=ft.Column([
            ft.Container(content=image, bgcolor="#1c2b24", padding=10, border_radius=8),
            numero
        ]),
        bgcolor="#eeeeee",
        padding=15,
        border_radius=15
    )

    controles = ft.Row([
        ft.ElevatedButton("Anterior", on_click=anterior, bgcolor="#212121", color="white"),
        ft.ElevatedButton("Siguiente", on_click=siguiente, bgcolor="#212121", color="white")
    ])

    busqueda = ft.Row([
        entrada,
        ft.ElevatedButton("Buscar", on_click=buscar, bgcolor="#ffeb3b", color="black")
    ])

    panel_izquierdo = ft.Container(
        content=ft.Column([luces, pantalla, controles, busqueda, mensaje]),
        bgcolor="#d32f2f",
        padding=20,
        width=360,
        border_radius=20
    )

    panel_derecho = ft.Container(
        content=ft.Column([
            nombre,
            ft.Text("TIPO", size=12, color="#ffcdd2"),
            tipos,
            ft.Text("ESTADÍSTICAS BASE", size=12, color="#ffcdd2"),
            estadisticas,
            ft.Text("DATOS", size=12, color="#ffcdd2"),
            datos,
            ft.Text("HABILIDADES", size=12, color="#ffcdd2"),
            habilidades
        ]),
        bgcolor="#b71c1c",
        padding=25,
        width=520,
        border_radius=20
    )

    page.add(ft.Row([panel_izquierdo, panel_derecho]))

    mostrar(pk.pokemon(1))


ft.app(target=main)