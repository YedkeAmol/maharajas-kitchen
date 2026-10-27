import os
import shutil

src_dir = r"C:\Users\Acer\.gemini\antigravity\brain\601f2e3f-87b6-4e55-85f7-a2e8820656b2"
dest_dir = os.path.join(os.path.dirname(__file__), "static", "img")
os.makedirs(dest_dir, exist_ok=True)

image_map = {
    "indian_thali_1788748695069.jpg": "indian_thali.jpg",
    "samosa_1788747737286.jpg": "samosa.jpg",
    "paneer_tikka_1788747811334.jpg": "paneer_tikka.jpg",
    "indian_starters_1788748586597.jpg": "indian_starters.jpg",
    "butter_chicken_1788747748208.jpg": "butter_chicken.jpg",
    "biryani_1788747835394.jpg": "biryani.jpg",
    "masala_dosa_1788747824618.jpg": "masala_dosa.jpg",
    "indian_breads_1788748548621.jpg": "indian_breads.jpg",
    "indian_desserts_1788748563034.jpg": "indian_desserts.jpg",
    "mango_lassi_1788747847225.jpg": "mango_lassi.jpg",
    "indian_drinks_1788748710493.jpg": "indian_drinks.jpg",
    "maharajas_kitchen_logo_1788748274076.jpg": "logo.jpg"
}

count = 0
for src_name, dest_name in image_map.items():
    src_path = os.path.join(src_dir, src_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(dest_dir, dest_name))
        count += 1

print(f"Success! Copied {count} images.")