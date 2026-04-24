import datetime
import math
import xml.etree.ElementTree as ET

LAT = 39.9612
LON = -82.9988
RSS_FILE = "solar_time.xml"

def equation_of_time(day_of_year):
    B = 2 * math.pi * (day_of_year - 81) / 364
    return 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

def compute_solar_time():
    now = datetime.datetime.utcnow()
    day_of_year = now.timetuple().tm_yday

    eot = equation_of_time(day_of_year)  # minutes
    longitude_correction = 4 * LON       # minutes

    total_correction = eot + longitude_correction
    solar_time = now + datetime.timedelta(minutes=total_correction)

    return solar_time.strftime("%H:%M:%S")

def generate_rss(solar_time):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Columbus Solar Time"
    ET.SubElement(channel, "link").text = "https://github.com"
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

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

def main():
    solar_time = compute_solar_time()
    generate_rss(solar_time)
    print(f"RSS feed updated. Solar time: {solar_time}")

if __name__ == "__main__":
    main()
    main()
