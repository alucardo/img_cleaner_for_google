import os
import subprocess
import piexif


def to_deg(value, loc):
    """
    Konwertuje stopnie dziesiętne na format EXIF i zwraca kierunek.
    loc: lista dwóch kierunków, np. ["S", "N"] dla szerokości
    """
    if value < 0:
        loc_value = loc[0]  # "S" lub "W"
    else:
        loc_value = loc[1]  # "N" or "E"

    abs_value = abs(value)
    deg = int(abs_value)
    min = int((abs_value - deg) * 60)
    sec = int((abs_value - deg - min / 60) * 3600 * 100)

    return [(deg, 1), (min, 1), (sec, 100)], loc_value

def change_gps_location_and_title(img_path, lat, lon, desc = ""):
    lat_val, lat_ref = to_deg(lat, ["S", "N"])
    lon_val, lon_ref = to_deg(lon, ["W", "E"])

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_ref,
        piexif.GPSIFD.GPSLatitude: lat_val,
        piexif.GPSIFD.GPSLongitudeRef: lon_ref,
        piexif.GPSIFD.GPSLongitude: lon_val,
    }

    zeroth_ifd = {
        # To zmienia pole "Opis"
        piexif.ImageIFD.ImageDescription: desc.encode('utf-8'),

        # To zmienia pole "Tytuł" (wykorzystuje tag XPTitle)
        piexif.ImageIFD.XPTitle: desc.encode('utf-16le')
    }

    exif_dict = {"0th": zeroth_ifd, "GPS": gps_ifd}

    try:
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, img_path)
        print(f"Zapisano dane dla {img_path}")
    except Exception as e:
        print(f"Błąd zapisu EXIF: {e}")

def clear_where_from(file_path):
    """Usuwa atrybuty rozszerzone macOS (pole 'Skąd')."""
    try:
        # Polecenie xattr -c usuwa wszystkie atrybuty rozszerzone pliku
        subprocess.run(['xattr', '-c', file_path], check=True)
    except Exception as e:
        print(f"Błąd podczas czyszczenia atrybutów dla {file_path}: {e}")


# --- KONFIGURACJA ---
path = "zdjecia"
try:
    lat = float(input("Podaj Latitude (szerokość, np. 52.2297): "))
    lon = float(input("Podaj Longitude (długość, np. 21.0122): "))
except ValueError:
    print("Błąd: Współrzędne muszą być liczbami!")

folder_path = "zdjecia"

for filename in os.listdir(folder_path):
    if filename.lower().endswith((".jpg", ".jpeg")):
        img_path = os.path.join(folder_path, filename)
        clear_where_from(img_path)
        user_desc = input(f"Podaj opis dla {filename} (enter = pusty): ")

        change_gps_location_and_title(img_path, lat, lon, user_desc)

