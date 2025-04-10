import os, json, re

IMAGE_DIR = "photos"
ALLOWED_EXT = (".png", ".jpg", ".jpeg", ".gif")

def extract_date(filename):
    # Cerca nel filename una data nel formato YYYY-MM-DD.
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None

manifest = []

# Scansione della directory principale
for entry in os.listdir(IMAGE_DIR):
    path = os.path.join(IMAGE_DIR, entry)
    if os.path.isdir(path):
        # Per gli album, si assume che il nome della cartella sia la data
        album_date = entry  # ad es. "2023-04-10"
        # Raccogli le immagini all’interno dell’album che rispettano il filtro
        images = [os.path.join(IMAGE_DIR, entry, f) 
                  for f in os.listdir(path) if f.lower().endswith(ALLOWED_EXT)]
        images.sort()
        if images:
            manifest.append({
                "type": "album",
                "name": entry,
                "date": album_date,
                "cover": images[0],
                "images": images
            })
    elif os.path.isfile(path) and entry.lower().endswith(ALLOWED_EXT):
        # Per le immagini singole, l'estrazione della data è fondamentale
        image_date = extract_date(entry)
        if image_date:
            manifest.append({
                "type": "image",
                "name": entry,
                "date": image_date,
                "url": os.path.join(IMAGE_DIR, entry)
            })
        else:
            print(f"Attenzione: {entry} non contiene una data nel filename!")
            
# Ordina il manifesto in ordine decrescente (più recenti prima) utilizzando la data
manifest.sort(key=lambda x: x["date"], reverse=True)

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=4)