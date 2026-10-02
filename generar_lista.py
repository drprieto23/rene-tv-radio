import urllib.request
import re

# ============================================================
# RENE TV + RADIO
# ============================================================

TV_URL = "https://iptv-org.github.io/iptv/countries/ar.m3u"


# ============================================================
# CANALES DE TV
# tvg-id : categoría
# ============================================================

CANALES = {

    # 📺 TV ABIERTA
    "TVPublica.ar": "📺 TV Abierta",
    "Telefe.ar": "📺 TV Abierta",
    "ElTrece.ar": "📺 TV Abierta",
    "AmericaTV.ar": "📺 TV Abierta",
    "ElNueve.ar": "📺 TV Abierta",
    "NETTV.ar": "📺 TV Abierta",

    # 📰 NOTICIAS
    "TodoNoticias.ar": "📰 Noticias",
    "C5N.ar": "📰 Noticias",
    "A24.ar": "📰 Noticias",
    "LaNacionPlus.ar": "📰 Noticias",
    "Canal26.ar": "📰 Noticias",
    "CronicaTV.ar": "📰 Noticias",

    # ⚽ DEPORTES
    "DeporTV.ar": "⚽ Deportes",

    # 🎬 CINE / CULTURA
    "CineAr.ar": "🎬 Cine y Series",
    "Encuentro.ar": "🎬 Cine y Series",

    # 👦 INFANTIL
    "Pakapaka.ar": "👦 Infantil",
}


# ============================================================
# STREAMS DE RESPALDO
#
# Sólo ponemos acá streams directos que una app IPTV
# pueda reproducir.
# ============================================================

RESPALDOS = {

    "TodoNoticias.ar": (
        "TN - Todo Noticias",
        "https://live-01-01-tn.vodgc.net/TN24/index.m3u8",
        "📰 Noticias"
    ),

}


# ============================================================
# RADIOS
# ============================================================

RADIOS = [

    (
        "Radio Mitre AM 790",
        "https://buecrplb01.cienradios.com.ar/Mitre790.aac"
    ),

    (
        "La 100 FM 99.9",
        "https://buecrplb01.cienradios.com.ar/la100.aac"
    ),

    (
        "Aspen FM 102.3",
        "https://24283.live.streamtheworld.com/ASPENAAC.aac"
    ),

    (
        "Rock & Pop FM 95.9",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/ROCKANDPOPAAC_SC"
    ),

    (
        "Mega FM 98.3",
        "https://mega.stweb.tv/mega983/live/playlist.m3u8"
    ),

    (
        "Radio 10 AM 710",
        "https://s6.stweb.tv/radio10/live/playlist.m3u8"
    ),

    (
        "Radio Rivadavia AM 630",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/RIVADAVIAAAC_SC"
    ),

    (
        "Continental AM 590",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/CONTINENTAL_SC"
    ),

    (
        "La Red AM 910",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/LA_RED_AM910AAC.aac"
    ),

    (
        "Blue FM 100.7",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/BLUE_FM_100_7AAC.aac"
    ),

    (
        "Radio Con Vos FM 89.9",
        "https://server1.stweb.tv/rcvos/live/playlist.m3u8"
    ),

    (
        "Metro",
        "https://playerservices.streamtheworld.com/api/livestream-redirect/METROAAC.aac"
    ),

    (
        "Vale FM 97.5",
        "https://s6.stweb.tv/vale/live/playlist.m3u8"
    ),

    (
        "AM 750",
        "https://mdstrm.com/audio/601bf3e463786007e6d3b9b0/icecast.audio"
    ),

    (
        "CNN Radio Argentina",
        "https://estudio.cnnradioargentina.com.ar/stream"
    ),
]


# ============================================================
# FUNCIONES
# ============================================================

def descargar(url):

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(
        req,
        timeout=30
    ) as respuesta:

        return respuesta.read().decode(
            "utf-8",
            errors="ignore"
        )


def obtener_tvg_id(linea):

    match = re.search(
        r'tvg-id="([^"]+)"',
        linea
    )

    if not match:
        return None

    tvg_id = match.group(1)

    # IPTV-org puede utilizar:
    #
    # A24.ar@SD
    # A24.ar@HD
    #
    # Nosotros trabajamos con el ID base.

    return tvg_id.split("@")[0]


def cambiar_grupo(linea, grupo):

    if 'group-title="' in linea:

        return re.sub(
            r'group-title="[^"]*"',
            f'group-title="{grupo}"',
            linea
        )

    return linea.replace(
        "#EXTINF:",
        f'#EXTINF: group-title="{grupo}" '
    )


# ============================================================
# DESCARGAR IPTV-ORG
# ============================================================

print("")
print("Descargando TV Argentina...")

tv = descargar(TV_URL)

lineas = tv.splitlines()


# ============================================================
# BUSCAR CANALES
# ============================================================

encontrados = {}

i = 0

while i < len(lineas):

    linea = lineas[i]

    if linea.startswith("#EXTINF"):

        tvg_id = obtener_tvg_id(linea)

        if tvg_id in CANALES:

            grupo = CANALES[tvg_id]

            linea_modificada = cambiar_grupo(
                linea,
                grupo
            )

            if i + 1 < len(lineas):

                stream = lineas[i + 1].strip()

                # Guardamos solamente la primera
                # variante encontrada.

                if tvg_id not in encontrados:

                    encontrados[tvg_id] = (
                        linea_modificada,
                        stream
                    )

    i += 1


# ============================================================
# GENERAR PLAYLIST
# ============================================================

contenido = ["#EXTM3U"]

usados_respaldo = []

faltantes = []


orden_grupos = [

    "📺 TV Abierta",
    "📰 Noticias",
    "⚽ Deportes",
    "🎬 Cine y Series",
    "👦 Infantil",

]


for grupo in orden_grupos:

    for tvg_id, grupo_canal in CANALES.items():

        if grupo_canal != grupo:
            continue

        # ----------------------------------------
        # Fuente principal IPTV-org
        # ----------------------------------------

        if tvg_id in encontrados:

            extinf, stream = encontrados[tvg_id]

            contenido.append(extinf)
            contenido.append(stream)

            continue


        # ----------------------------------------
        # Fuente de respaldo
        # ----------------------------------------

        if tvg_id in RESPALDOS:

            nombre, stream, grupo_respaldo = (
                RESPALDOS[tvg_id]
            )

            contenido.append(
                f'#EXTINF:-1 '
                f'tvg-id="{tvg_id}" '
                f'group-title="{grupo_respaldo}",'
                f'{nombre}'
            )

            contenido.append(stream)

            usados_respaldo.append(tvg_id)

            continue


        # ----------------------------------------
        # No encontramos el canal
        # ----------------------------------------

        faltantes.append(tvg_id)


# ============================================================
# RADIOS
# ============================================================

for nombre, url in RADIOS:

    contenido.append(
        '#EXTINF:-1 '
        'group-title="📻 Radios",'
        f'{nombre}'
    )

    contenido.append(url)


# ============================================================
# GUARDAR ARCHIVO
# ============================================================

ARCHIVO_SALIDA = "rene-tv-radio.m3u"

with open(
    ARCHIVO_SALIDA,
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "\n".join(contenido) + "\n"
    )


# ============================================================
# INFORME
# ============================================================

print("")
print("====================================")
print("       RENE TV + RADIO")
print("====================================")
print("")

print(
    f"TV desde IPTV-org : {len(encontrados)}"
)

print(
    f"TV desde respaldo : {len(usados_respaldo)}"
)

print(
    f"Radios             : {len(RADIOS)}"
)

print(
    f"TV faltantes       : {len(faltantes)}"
)


if usados_respaldo:

    print("")
    print("🔄 Canales usando respaldo:")

    for canal in usados_respaldo:
        print(" -", canal)


if faltantes:

    print("")
    print("⚠️ Canales todavía no encontrados:")

    for canal in faltantes:
        print(" -", canal)

else:

    print("")
    print("✅ Todos los canales fueron encontrados.")


print("")
print(
    f"Archivo generado: {ARCHIVO_SALIDA}"
)

print("")
