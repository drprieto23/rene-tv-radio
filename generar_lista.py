import urllib.request

TV_URL = "https://iptv-org.github.io/iptv/countries/ar.m3u"

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


print("Descargando TV Argentina...")
tv = descargar(TV_URL)

contenido = ["#EXTM3U"]

# TV
for linea in tv.splitlines():
    if linea.strip() != "#EXTM3U":
        contenido.append(linea)

# Radios
for nombre, url in RADIOS:
    contenido.append(
        f'#EXTINF:-1 group-title="📻 Radios Argentina",{nombre}'
    )
    contenido.append(url)

with open("rene-tv-radio.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(contenido) + "\n")

print("Lista creada correctamente.")
print(f"Radios incluidas: {len(RADIOS)}")
