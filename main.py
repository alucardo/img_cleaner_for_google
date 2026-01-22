import os
import subprocess


def update_metadata(img_path, lat, lon, text, desc):
    # 1. Usuwanie atrybutów systemowych macOS ("Skąd")
    try:
        subprocess.run(['xattr', '-c', img_path], check=True)
    except:
        pass

    cmd = [
        'exiftool',
        '-all=',
        f'-Title={text}',
        f'-Description={desc}',
        f'-ObjectName={text}',
        f'-Caption-Abstract={text}',
        f'-GPSLatitude={lat}',
        f'-GPSLongitude={lon}',
        '-GPSLatitudeRef=N' if float(lat) >= 0 else '-GPSLatitudeRef=S',
        '-GPSLongitudeRef=E' if float(lon) >= 0 else '-GPSLongitudeRef=W',
        '-overwrite_original',
        img_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Sukces: {os.path.basename(img_path)}")
    except subprocess.CalledProcessError as e:
        print(f"Błąd ExifTool dla {img_path}: {e}")


# --- KONFIGURACJA ---
folder_path = "zdjecia"

if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' nie istnieje!")
else:
    try:
        lat_in = input("Podaj Latitude: ")
        lon_in = input("Podaj Longitude: ")

        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".jpeg")):
                full_path = os.path.join(folder_path, filename)
                user_text = input(f"Podaj tytuł dla {filename}: ")
                user_desc = input(f"Podaj opis dla {filename}: ")
                update_metadata(full_path, lat_in, lon_in, user_text, user_desc)

    except Exception as e:
        print(f"Wystąpił błąd: {e}")