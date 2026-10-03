import urllib.request
import re

# ============================================================
# RENE TV + RADIO - Generador V3.1
# ============================================================
#
# Prioridad para canales de TV:
#
# 1. Streams preferidos probados manualmente
# 2. IPTV-org
# 3. Streams de respaldo
#
# Además genera:
#
# - Radios
# - Música
# - Espacio / NASA
# - Futuros videos de fútbol y clásicos
#
# ============================================================


FUENTE_TV = "https://iptv-org.github.io/iptv/countries/ar.m3u"
ARCHIVO_SALIDA = "rene-tv-radio.m3u"


# ============================================================
# CANALES DE IPTV-ORG QUE QUEREMOS
# ============================================================

CANALES = {

    # --------------------------------------------------------
    # TV ABIERTA
    # --------------------------------------------------------

    "TVPublica.ar": "📺 TV Abierta",
    "Telefe.ar": "📺 TV Abierta",
    "ElTrece.ar": "📺 TV Abierta",
    "AmericaTV.ar": "📺 TV Abierta",
    "ElNueve.ar": "📺 TV Abierta",
    "NETTV.ar": "📺 TV Abierta",

    # --------------------------------------------------------
    # NOTICIAS
    # --------------------------------------------------------

    "TodoNoticias.ar": "📰 Noticias",
    "C5N.ar": "📰 Noticias",
    "A24.ar": "📰 Noticias",
    "LaNacionPlus.ar": "📰 Noticias",
    "Canal26.ar": "📰 Noticias",
    "CronicaTV.ar": "📰 Noticias",

    # --------------------------------------------------------
    # DEPORTES
    # --------------------------------------------------------

    "DeporTV.ar": "⚽ Deportes",

    # --------------------------------------------------------
    # CINE / CULTURA
    # --------------------------------------------------------

    "CineAr.ar": "🎬 Cine y Series",
    "Encuentro.ar": "🎬 Cine y Series",

    # --------------------------------------------------------
    # INFANTIL
    # --------------------------------------------------------

    "Pakapaka.ar": "👦 Infantil",
}


# ============================================================
# STREAMS PREFERIDOS
#
# Estos NO dependen de IPTV-org.
#
# Son streams que probamos manualmente y queremos utilizar
# siempre que generemos la lista.
# ============================================================

STREAMS_PREFERIDOS = {

    # --------------------------------------------------------
    # TV ABIERTA
    # --------------------------------------------------------

    "ElTrece.ar": (
        "El Trece",
        "https://live-01-02-eltrece.vodgc.net/eltrecetv/index.m3u8",
        "📺 TV Abierta"
    ),

    "TVPublica.ar": (
        "TV Pública",
        "http://playcom.trapemn.tv:1935/transcoderip/tvpublica.stream/playlist.m3u8",
        "📺 TV Abierta"
    ),

    # --------------------------------------------------------
    # CANALES ADICIONALES
    # --------------------------------------------------------

    "+Perfil.ar": (
        "+Perfil",
        "https://unlimited1-us.dps.live/perfiltv/perfiltv.smil/perfiltv/livestream2/chunks.m3u8",
        "📰 Noticias"
    ),

    "TVUniversidad.ar": (
        "TV Universidad",
        "https://stratus.stream.cespi.unlp.edu.ar/hls/tvunlp.m3u8",
        "📺 TV Abierta"
    ),
}


# ============================================================
# RESPALDOS
#
# Sólo se utilizan cuando:
#
# - No existe un stream preferido.
# - IPTV-org no encuentra el canal.
#
# Por ahora lo dejamos vacío.
#
# No agregamos URLs dudosas, tokenizadas o que comprobamos
# manualmente que no funcionan.
# ============================================================

RESPALDOS = {
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
# VIDEOS
# ============================================================
#
# Formato:
#
# (
#     "Nombre",
#     "URL directa",
#     "Grupo"
# )
#
# Los MP4 propios pueden alojarse en Cloudflare R2.
#
# ============================================================

VIDEOS = [

    # --------------------------------------------------------
    # MUSICA
    # --------------------------------------------------------

    (
        "Eminem ft. Dido - Stan",
        "https://pub-550ee302d2584029bb999695b2374b2d.r2.dev/Eminem-Stan-Short-Version-ft-Dido_Media_aSLZFdqwh7E_001_1080p.mp4",
        "🎸 Música"
    ),

    # --------------------------------------------------------
    # ESPACIO / NASA
    # --------------------------------------------------------

    (
        "NASA - De la Luna a la Tierra",
        "https://svs.gsfc.nasa.gov/vis/a000000/a005000/a005039/moon_to_earth_1080p30.mp4",
        "🚀 Espacio"
    ),

    (
        "NASA - Viaje a un agujero negro",
        "https://svs.gsfc.nasa.gov/vis/a010000/a014500/a014576/14576_BHPlunge_Explainer_1080.mp4",
        "🚀 Espacio"
    ),
]


# ============================================================
# FUNCIONES
# ============================================================

def descargar_lista():

    print("Descargando IPTV-org...")

    request = urllib.request.Request(
        FUENTE_TV,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as respuesta:

        return respuesta.read().decode(
            "utf-8",
            errors="ignore"
        )


def obtener_tvg_id(linea):

    """
    IPTV-org puede devolver IDs como:

        A24.ar@SD
        A24.ar@HD

    Para nosotros ambos corresponden a:

        A24.ar
    """

    match = re.search(
        r'tvg-id="([^"]+)"',
        linea
    )

    if not match:
        return None

    return match.group(1).split("@")[0]


def cambiar_grupo(linea, grupo):

    """
    Reemplaza group-title si ya existe.

    Si no existe, lo agrega.
    """

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


def crear_entrada(
    nombre,
    url,
    grupo,
    tvg_id=""
):

    return [

        (
            f'#EXTINF:-1 '
            f'tvg-id="{tvg_id}" '
            f'group-title="{grupo}",'
            f'{nombre}'
        ),

        url
    ]


# ============================================================
# GENERAR LISTA
# ============================================================

def generar():

    contenido = descargar_lista()

    lineas = contenido.splitlines()

    encontrados_iptv = {}

    salida = [
        "#EXTM3U"
    ]


    # ========================================================
    # BUSCAR CANALES EN IPTV-ORG
    # ========================================================

    i = 0

    while i < len(lineas):

        linea = lineas[i]

        if linea.startswith("#EXTINF"):

            tvg_id = obtener_tvg_id(linea)

            if tvg_id in CANALES:

                if i + 1 < len(lineas):

                    url = lineas[i + 1].strip()

                    # Guardamos solamente la primera versión
                    # encontrada de cada canal.

                    if tvg_id not in encontrados_iptv:

                        encontrados_iptv[tvg_id] = (
                            linea,
                            url
                        )

        i += 1


    # ========================================================
    # ESTADISTICAS
    # ========================================================

    estadisticas = {

        "preferido": [],
        "iptv": [],
        "respaldo": [],
        "faltante": []
    }


    # ========================================================
    # AGREGAR CANALES PRINCIPALES
    #
    # Prioridad:
    #
    # 1 - Stream preferido
    # 2 - IPTV-org
    # 3 - Respaldo
    # ========================================================

    for tvg_id, grupo in CANALES.items():


        # ----------------------------------------------------
        # 1. STREAM PREFERIDO
        # ----------------------------------------------------

        if tvg_id in STREAMS_PREFERIDOS:

            nombre, url, grupo_preferido = (
                STREAMS_PREFERIDOS[tvg_id]
            )

            salida.extend(
                crear_entrada(
                    nombre,
                    url,
                    grupo_preferido,
                    tvg_id
                )
            )

            estadisticas["preferido"].append(
                tvg_id
            )

            continue


        # ----------------------------------------------------
        # 2. IPTV-ORG
        # ----------------------------------------------------

        if tvg_id in encontrados_iptv:

            linea_extinf, url = (
                encontrados_iptv[tvg_id]
            )

            linea_extinf = cambiar_grupo(
                linea_extinf,
                grupo
            )

            salida.append(
                linea_extinf
            )

            salida.append(
                url
            )

            estadisticas["iptv"].append(
                tvg_id
            )

            continue


        # ----------------------------------------------------
        # 3. RESPALDO
        # ----------------------------------------------------

        if tvg_id in RESPALDOS:

            nombre, url, grupo_respaldo = (
                RESPALDOS[tvg_id]
            )

            salida.extend(
                crear_entrada(
                    nombre,
                    url,
                    grupo_respaldo,
                    tvg_id
                )
            )

            estadisticas["respaldo"].append(
                tvg_id
            )

            continue


        # ----------------------------------------------------
        # NO ENCONTRADO
        # ----------------------------------------------------

        estadisticas["faltante"].append(
            tvg_id
        )


    # ========================================================
    # CANALES ADICIONALES PREFERIDOS
    #
    # Son canales nuestros que no forman parte de CANALES
    # y que queremos agregar directamente.
    #
    # Ej:
    #
    # +Perfil
    # TV Universidad
    #
    # ========================================================

    for tvg_id, datos in STREAMS_PREFERIDOS.items():

        if tvg_id not in CANALES:

            nombre, url, grupo = datos

            salida.extend(
                crear_entrada(
                    nombre,
                    url,
                    grupo,
                    tvg_id
                )
            )

            estadisticas["preferido"].append(
                tvg_id
            )


    # ========================================================
    # RADIOS
    # ========================================================

    for nombre, url in RADIOS:

        salida.extend(
            crear_entrada(
                nombre,
                url,
                "📻 Radios"
            )
        )


    # ========================================================
    # VIDEOS
    # ========================================================

    for nombre, url, grupo in VIDEOS:

        salida.extend(
            crear_entrada(
                nombre,
                url,
                grupo
            )
        )


    # ========================================================
    # GUARDAR ARCHIVO
    # ========================================================

    with open(
        ARCHIVO_SALIDA,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            "\n".join(salida) + "\n"
        )


    # ========================================================
    # RESUMEN
    # ========================================================

    print()
    print(
        "============================================"
    )

    print(
        " RENE TV + RADIO - V3.1"
    )

    print(
        "============================================"
    )

    print()

    print(
        f"TV stream preferido : "
        f"{len(estadisticas['preferido'])}"
    )

    print(
        f"TV desde IPTV-org   : "
        f"{len(estadisticas['iptv'])}"
    )

    print(
        f"TV desde respaldo   : "
        f"{len(estadisticas['respaldo'])}"
    )

    print(
        f"TV faltantes        : "
        f"{len(estadisticas['faltante'])}"
    )

    print(
        f"Radios              : "
        f"{len(RADIOS)}"
    )

    print(
        f"Videos              : "
        f"{len(VIDEOS)}"
    )

    print()


    # --------------------------------------------------------
    # STREAMS PREFERIDOS
    # --------------------------------------------------------

    if estadisticas["preferido"]:

        print(
            "Streams preferidos:"
        )

        for canal in estadisticas["preferido"]:

            print(
                f"  OK  {canal}"
            )

        print()


    # --------------------------------------------------------
    # STREAMS DE RESPALDO
    # --------------------------------------------------------

    if estadisticas["respaldo"]:

        print(
            "Streams de respaldo:"
        )

        for canal in estadisticas["respaldo"]:

            print(
                f"  OK  {canal}"
            )

        print()


    # --------------------------------------------------------
    # CANALES FALTANTES
    # --------------------------------------------------------

    if estadisticas["faltante"]:

        print(
            "Canales no encontrados:"
        )

        for canal in estadisticas["faltante"]:

            print(
                f"  --  {canal}"
            )

        print()


    # --------------------------------------------------------
    # VIDEOS
    # --------------------------------------------------------

    if VIDEOS:

        print(
            "Videos agregados:"
        )

        for nombre, url, grupo in VIDEOS:

            print(
                f"  OK  {grupo} - {nombre}"
            )

        print()


    print(
        f"Archivo generado: "
        f"{ARCHIVO_SALIDA}"
    )

    print(
        "============================================"
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    generar()
