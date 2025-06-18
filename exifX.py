import argparse
from PIL.ExifTags import TAGS
from PIL import Image
from datetime import datetime
import os
from typing import Dict, Optional
import hashlib
def display_banner():
    banner = r"""
                                                           
     ______                    ____       _____                  
 ___|\     \  _____      _____|    | ____|\    \ _____      _____
|     \     \ \    \    /    /|    ||    | \    \\    \    /    /
|     ,_____/| \    \  /    / |    ||    |______/ \    \  /    / 
|     \--'\_|/  \____\/____/  |    ||    |----'\   \___\/____/  
|     /___/|    /    /\    \  |    ||    |_____/   /    /\    \  
|     \____|\  /    /  \    \ |    ||    |        /    /  \    \ 
|____ '     /|/____/ /\ \____\|____||____|       /____/ /\ \____\
|    /_____/ ||    |/  \|    ||    ||    |       |    |/  \|    |
|____|     | /|____|    |____||____||____|       |____|    |____|
  \( |_____|/   \(        )/    \(    )/           \(        )/  
   '    )/       '        '      '    '             '        '   
        '   

                    🔍  ExifX — EXIF Metadata Extractor
                           by @yadneshx17
    """
    print(banner)

Osint_tags = {
    "Make", "Model", "SerialNumber", "LensModel", "Software",
}

def calculate_file_hashes(file_path: str) -> Dict[str, str]:
    """Calculate MD5 and SHA-256 hashes of a file."""
    hashes = {}
    try:
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files efficiently
            md5_hash = hashlib.md5() # objs
            sha256_hash = hashlib.sha256()
            chunk_size = 8192
            while chunk := f.read(chunk_size):
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
            hashes['MD5'] = md5_hash.hexdigest()
            hashes['SHA-256'] = sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating hashes: {e}")
    return hashes

def format_datetime(dt_str: str) -> str:
    """Format datetime string into a more readable format."""
    try:    
        # dt = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
        # return dt.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S").strftime("%d %b %Y, %I:%M %p")

    except Exception:
        return dt_str
    
def exif_View(image_path: str):
    exif = {}
    img = Image.open(image_path)

    if img._getexif() is not None:
        for tag, value in img._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value

    print(f"\n{'='*20} File Information {'='*20}\n")
    print(f"File: {os.path.basename(image_path)}")
    print(f"Size: {os.path.getsize(image_path) / 1024:.2f} KB")
    print(f"Dimensions: {img.size[0]}x{img.size[1]} pixels")
    print(f"Format: {img.format}")

    # Calculate file hashes.
    print("\n========== File Hashes ==========\n")
    hashes = calculate_file_hashes(image_path)
    for hash_type, hash_value in hashes.items():
        print(f"{hash_type}: {hash_value}")


    print(f"\n{'='*20} GPS Info {'='*20}") 
    
    if "GPSInfo" in exif:
        gps_info = exif["GPSInfo"]

        def convert_to_degrees(value):
            """
            Notees:
            Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format.
            Args:
                value (tuple): The GPS coordinate as a tuple (degrees, minutes, seconds)
            Returns:
                float: The coordinate in degrees
            """
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)

        # Convert latitude and longitude to degrees
        lat = convert_to_degrees(gps_info[2])
        lon = convert_to_degrees(gps_info[4])
        lat_ref = gps_info[1]
        lon_ref = gps_info[3]

        # Adjust the sign of the coordinates based on the reference (N/S, E/W)
        if lat_ref != "N":
            lat = -lat
        if lon_ref != "E":
            lon = -lon

        # Format the GPS coordinates into a human-readable string
        geo_coordinate = "{0}° {1}, {2}° {3}".format(lat, lat_ref, lon, lon_ref)
        print(f"GPS Cordinates: {geo_coordinate}")

        # Create a Google Maps link
        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        print(f"Google Maps link:> {google_maps_link}")
    else:
        print("No GPS information found.")

    if "DateTime" in exif:
        value = exif["DateTime"]
        if isinstance(value, str):
            print(f"Date Taken: {format_datetime(value)}")
        else:
            print("DateTime exists but is not a string. May be corrupte")
        
    else:
        print("No DateTime found.")

    print(f"\n{'='*20} Device Info {'='*20}")
    tags_of_interest = [
        "Make", "Model", "Software", "ExposureTime", "FNumber",
        "ISOSpeedRatings", "Flash", "FocalLength", "WhiteBalance"
    ]

    for tag in tags_of_interest:
        if tag in exif:
            print(f"{tag}: {exif[tag]}")

def main():
    parser = argparse.ArgumentParser(description="Extract EXIF metadata from an image.")
    parser.add_argument("image", help="Path to the image file")
    args = parser.parse_args()

    display_banner()
    exif_View(args.image)


if __name__ == "__main__":
    main()