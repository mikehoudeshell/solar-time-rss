import requests
import datetime
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
LAT = 39.9612
LON = -82.9988
RSS_FILE = "solar_time.xml"

API_URL = (
    f"https://api.open-meteo.com/v1/astronomy?"
    f"latitude={LAT}&longitude={LON}&hourly=solar_time"
)

HEADERS = {
    "User-Agent": "SolarTimeRSSBot/1.0 (https://github.com/your-username)"
}

def fetch_solar_time():
    """Fetch the current solar time from Open-Meteo."""
    try:
        r = requests.get(API_URL, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch solar time: {e}")

    times = data["hourly"]["time"]
    solar_times = data["hourly"]["solar_time"]

    now = datetime.datetime.utcnow().replace(second=0, microsecond=0).isoformat()

    if now in times:
        idx = times.index(now)
        return solar_times[idx]

    dt_now = datetime.datetime.utcnow()
    closest_idx = min(
        range(len(times)),
        key=lambda i: abs(datetime.datetime.fromisoformat(times[i]) - dt_now)
    )
    return solar_times[closest_idx]

def generate_rss(solar_time):
    """Generate RSS XML content."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Columbus Solar Time"
    ET.SubElement(channel, "link").text = "https://api.open-meteo.com/"
    ET.SubElement(channel, "description").text = "Real-time solar time for Columbus, Ohio"
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = "Current Solar Time"
    ET.SubElement(item, "description").text = f"Solar time is: {solar_time}"
    ET.SubElement(item, "pubDate").text = datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    ET.SubElement(item, "guid").text = "solar-time-columbus"

    indent_xml(rss)

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

def indent_xml(elem, level=0):
    """Pretty-print XML for cleaner diffs."""
    indent = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent

def main():
    solar_time = fetch_solar_time()
    generate_rss(solar_time)
    print(f"RSS feed updated. Solar time: {solar_time}")

if __name__ == "__main__":
    main()
