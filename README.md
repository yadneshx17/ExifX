
# ExifX - Exif Metadata Extractor
A simple Python tool to extract and display Exif metadata from image files. It includes, date taken, camera details, and file hashes for integrity checks. Built with Osint and digital forensics in mind.

---
**🧰Features**:
- Extracts basic image info: size, format, dimensions
- Retrives and prints EXIF metadata
- Converts GPS coordinates to human-readable format
- Generates a Google Maps link for location data
-  Displays camera info (Make, Model, Focal Length, etc.)
-  Calculates file hashes (MD5, SHA1, SHA256)
-  Useful for OSINT, cybersecurity investigations, and metadata analysis
---
 🚀 Installation
 ```bash
git clone https://github.com/yadneshx17/ExifX.git
cd ExifX
pip install -r requirements.txt
 ```
---
📦 Usage
```bash
python exifX.py path/to/image.jpg
```
The output includes:
-   File size and dimensions
-   EXIF metadata (DateTime, Camera info, GPS)
-   Google Maps link (if GPS is found)
-   Cryptographic hashes of the file
