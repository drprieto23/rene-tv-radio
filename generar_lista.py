import urllib.request
import re

TV_URL = "https://iptv-org.github.io/iptv/countries/ar.m3u"

# Canales que queremos conservar.
# Clave = tvg-id de IPTV-org
# Valor = grupo que queremos mostrar en nuestra lista
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

    # 👦 OTROS
    "Pakapaka.ar": "👦 Infantil",
}


RADIOS = [
    ("Radio Mitre AM 790",
     "https://buecrplb01.cienradios.com.ar/Mitre790.aac"),

    ("La 100 FM 99.9",
     "https://buecrplb01.cienradios.com.ar/la100.aac"),

    ("Aspen FM 102.3",
     "https://24283.live.streamtheworld.com/ASPENAAC.aac"),

    ("Rock & Pop FM 95.9",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/ROCKANDPOPAAC_SC"),

    ("Mega FM 98.3",
     "https://mega.stweb.tv/mega983/live/playlist.m3u8"),

    ("Radio 10 AM 710",
     "https://s6.stweb.tv/radio10/live/playlist.m3u8"),

    ("Radio Rivadavia AM 630",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/RIVADAVIAAAC_SC"),

    ("Continental AM 590",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/CONTINENTAL_SC"),

    ("La Red AM 910",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/LA_RED_AM910AAC.aac"),

    ("Blue FM 100.7",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/BLUE_FM_100_7AAC.aac"),

    ("Radio Con Vos FM 89.9",
     "https://server1.stweb.tv/rcvos/live/playlist.m3u8"),

    ("Metro",
     "https://playerservices.streamtheworld.com/api/livestream-redirect/METROAAC.aac"),

    ("Vale FM 97.5",
     "https://s6.stweb.tv/vale/live/playlist.m3u8"),

    ("AM 750",
     "https://mdstrm.com/audio/601bf3e463786007e6d3b9b0/icecast.audio"),

    ("CNN Radio Argentina",
     "https://estudio.cnnradioargentina.com.ar/stream"),
]


def descargar(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def obtener_tvg_id(linea):
    match = re.search(r'tvg-id="([^"]+)"', linea)

    if match:
        return match.group(1)

    return None


print("Descargando TV Argentina...")
tv = descargar(TV_URL)

lineas = tv.splitlines()

encontrados = {}
faltantes = set(CANALES.keys())

i = 0

while i < len(lineas):

    linea = lineas[i]

    if linea.startswith("#EXTINF"):

        tvg_id = obtener_tvg_id(linea)

        if tvg_id in CANALES:

            grupo = CANALES[tvg_id]

            # Reemplazamos la categoría original
            if 'group-title="' in linea:

                linea = re.sub(
                    r'group-title="[^"]*"',
                    f'group-title="{grupo}"',
                    linea
                )

            else:

                linea = linea.replace(
                    "#EXTINF:",
                    f'#EXTINF: group-title="{grupo}" '
                )

            # URL del stream
            if i + 1 < len(lineas):

                encontrados[tvg_id] = (
                    linea,
                    lineas[i + 1]
                )

                faltantes.discard(tvg_id)

    i += 1


contenido = ["#EXTM3U"]


# --------------------------------
# TV
# --------------------------------

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

        if tvg_id in encontrados:

            extinf, stream = encontrados[tvg_id]

            contenido.append(extinf)
            contenido.append(stream)


# --------------------------------
# RADIOS
# --------------------------------

for nombre, url in RADIOS:

    contenido.append(
        f'#EXTINF:-1 group-title="📻 Radios",{nombre}'
    )

    contenido.append(url)


# --------------------------------
# GUARDAR
# --------------------------------

with open(
    "rene-tv-radio.m3u",
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(contenido) + "\n")


print("")
print("================================")
print(" RENE TV + RADIO")
print("================================")

print(f"Canales encontrados: {len(encontrados)}")
print(f"Radios: {len(RADIOS)}")

if faltantes:

    print("")
    print("⚠️ Canales no encontrados:")

    for canal in sorted(faltantes):
        print(" -", canal)

else:

    print("")
    print("✅ Todos los canales fueron encontrados.")
