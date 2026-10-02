import urllib.request
import re

TV_URL = "https://iptv-org.github.io/iptv/countries/ar.m3u"
RADIO_URL = "https://mammoli.ar/radio/api/playlist.m3u"

RADIOS = [
    "Mitre",
    "La 100",
    "Aspen",
    "Rock & Pop",
    "Mega",
    "Radio 10",
    "Rivadavia",
    "Continental",
    "La Red",
    "Pop",
    "Urbana Play",
    "Vorterix",
    "Blue"
]

def descargar(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def filtrar_radios(m3u):
    lineas = m3u.splitlines()
    resultado = []

    for i, linea in enumerate(lineas):
        if linea.startswith("#EXTINF"):
            nombre = linea.rsplit(",", 1)[-1].strip()

            if any(
                re.search(re.escape(radio), nombre, re.IGNORECASE)
                for radio in RADIOS
            ):
                # Cambiamos/añadimos el grupo
                if 'group-title="' in linea:
                    linea = re.sub(
                        r'group-title="[^"]*"',
                        'group-title="📻 Radios Argentina"',
                        linea
                    )
                else:
                    linea = linea.replace(
                        "#EXTINF:",
                        '#EXTINF: group-title="📻 Radios Argentina" '
                    )

                resultado.append(linea)

                if i + 1 < len(lineas):
                    resultado.append(lineas[i + 1])

    return resultado


print("Descargando TV Argentina...")
tv = descargar(TV_URL)

print("Descargando radios...")
radios = descargar(RADIO_URL)

radios_filtradas = filtrar_radios(radios)

# Quitamos el encabezado original de TV
tv_lineas = [
    linea for linea in tv.splitlines()
    if linea.strip() != "#EXTM3U"
]

contenido = ["#EXTM3U"]

contenido.append(
    '#EXTINF:-1 group-title="──────── TV ARGENTINA ────────",📺 TV ARGENTINA'
)
contenido.append("")

contenido.extend(tv_lineas)

contenido.append(
    '#EXTINF:-1 group-title="──────── RADIOS ────────",📻 RADIOS ARGENTINA'
)
contenido.append("")

contenido.extend(radios_filtradas)

with open("rene-tv-radio.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(contenido))

print(f"Lista creada con {len(radios_filtradas)//2} radios.")
