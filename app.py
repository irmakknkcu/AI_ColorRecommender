from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import os
from sklearn.cluster import KMeans

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_dominant_colors(image_path, n_colors=5):
    img = Image.open(image_path)
    img = img.resize((150, 150)) 
    img = img.convert("RGB")
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    counts = np.bincount(kmeans.labels_)
    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = [tuple(map(int, kmeans.cluster_centers_[i])) for i in sorted_indices]
    
    
    print("\n--- AI GÖZÜNDEN RESİM ANALİZİ ---")
    for i, color in enumerate(dominant_colors):
        print(f"Renk {i+1}: RGB{color}")
    print("-----------------------------------\n")
    
    return dominant_colors


def classify_and_recommend(rgb_list):
    
    
    for rgb in rgb_list:
        r, g, b = rgb
        max_val = max(rgb)
        min_val = min(rgb)
        diff = max_val - min_val

        
        if r > g + 20 and b > g + 20:
             if diff > 30: 
                 return "Purple / Royal", get_db()["Purple / Royal"]

        
        if g > r and g > b:
            if diff > 25 and g > 80 and g > r + 10:
                return "Green / Nature", get_db()["Green / Nature"]
        
        
        if b > r and b > g:
            if diff > 25 and b > 80:
                return "Blue / Cool", get_db()["Blue / Cool"]


    
    for rgb in rgb_list:
        r, g, b = rgb
        diff = max(rgb) - min(rgb)
        if r > g and r > b:
            if diff > 45: 
                if g > b + 40: return "Orange / Brown", get_db()["Orange / Brown"]
                elif r > g + 40: return "Pink / Red", get_db()["Pink / Red"]

    
    dom_rgb = rgb_list[0]
    max_val = max(dom_rgb)
    if max_val > 230: return "White / Bright", get_db()["White / Bright"]
    elif max_val < 50: return "Dark / Bold", get_db()["Dark / Bold"]
    
    return "Beige / Cream", get_db()["Beige / Cream"]


def get_db():
    return {
        "White / Bright": {
            "message": "Clean and bright atmosphere.",
            "palette": [
                {"hex": "#2F4F4F", "name": "Dark Slate"},
                {"hex": "#8B4513", "name": "Wood Brown"},
                {"hex": "#D4AF37", "name": "Gold Accent"}
            ],
            "furniture": ["Natural oak unit", "Rattan chair", "Soft grey sofa"],
            "accessories": ["Gold art", "White vases", "Linen curtains"],
            "lighting": ["Warm LED", "Gold lamp"],
            "wall": ["Farrow & Ball – Pointing", "Dulux – Soft Almond"]
        },
        "Neutral Grey": {
            "message": "Modern and balanced neutral tone.",
            "palette": [
                {"hex": "#FFDAB9", "name": "Peach"},
                {"hex": "#E6E6FA", "name": "Lavender"},
                {"hex": "#98FB98", "name": "Pale Green"}
            ],
            "furniture": ["Dark grey L-sofa", "Black metal table", "Oak stand"],
            "accessories": ["Lavender pillows", "Black frames", "Plants"],
            "lighting": ["Spotlights", "Frosted lamp"],
            "wall": ["Dulux – Foggy Grey", "Jotun – Modern Grey"]
        },
        "Beige / Cream": {
            "message": "Warm, cozy Japandi tone.",
            "palette": [
                {"hex": "#556B2F", "name": "Olive Green"},
                {"hex": "#8B4513", "name": "Dark Wood"},
                {"hex": "#FFF8DC", "name": "Cornsilk"}
            ],
            "furniture": ["Beige linen sofa", "Oak table", "Walnut unit"],
            "accessories": ["Wicker baskets", "Cream pillows", "Olive rug"],
            "lighting": ["Bamboo lamp", "Fabric shade"],
            "wall": ["Jotun – Washed Linen", "Dulux – Creamy"]
        },
        "Pink / Red": {
            "message": "Energetic and romantic tone.",
            "palette": [
                {"hex": "#F5F5F5", "name": "Soft White"},
                {"hex": "#808080", "name": "Grey"},
                {"hex": "#BC8F8F", "name": "Rosy Brown"}
            ],
            "furniture": ["Grey sofa", "Rose-gold table", "White shelves"],
            "accessories": ["Blush cushions", "Silver mirror", "Pink curtains"],
            "lighting": ["Rose chandelier", "Soft lamp"],
            "wall": ["Dulux – Soft Rose", "Jotun – Blush"]
        },
        "Orange / Brown": {
            "message": "Warm and earthy.",
            "palette": [
                {"hex": "#F0E68C", "name": "Khaki"},
                {"hex": "#F5F5DC", "name": "Beige"},
                {"hex": "#2E8B57", "name": "Sea Green"}
            ],
            "furniture": ["Dark oak unit", "Brown sofa", "Emerald chair"],
            "accessories": ["Brown pillows", "Patterned rugs", "Plants"],
            "lighting": ["Warm pendant", "Wood lamp"],
            "wall": ["Jotun – Wheat", "Dulux – Warm Sand"]
        },
        "Green / Nature": {
            "message": "Fresh and peaceful vibe.",
            "palette": [
                {"hex": "#8B4513", "name": "Wood Brown"},
                {"hex": "#FFFDD0", "name": "Cream"},
                {"hex": "#FF6347", "name": "Coral"}
            ],
            "furniture": ["White linen sofa", "Black bookshelf", "Walnut table"],
            "accessories": ["Beige cushions", "Lots of Plants", "Organic decor"],
            "lighting": ["Wooden pendant", "Fabric lamp"],
            "wall": ["Dulux – Pale Green", "Jotun – Minty Breeze"]
        },
        "Blue / Cool": {
            "message": "Calming and clean tone.",
            "palette": [
                {"hex": "#FFDAB9", "name": "Peach"},
                {"hex": "#FFFFFF", "name": "Pure White"},
                {"hex": "#C0C0C0", "name": "Silver"}
            ],
            "furniture": ["White TV unit", "Light grey sofa", "Wood table"],
            "accessories": ["Peach pillows", "Silver decor", "White curtains"],
            "lighting": ["Cool chandelier", "Minimal lamp"],
            "wall": ["Jotun – Airy Blue", "Dulux – Cool Breeze"]
        },
        "Purple / Royal": {
            "message": "Luxurious, creative and royal vibe.",
            "palette": [
                {"hex": "#FFD700", "name": "Gold Accent"},
                {"hex": "#C0C0C0", "name": "Silver"},
                {"hex": "#F5F5F5", "name": "Soft White"}
            ],
            "furniture": ["Velvet sofa", "Gold metal table", "Dark wood cabinet"],
            "accessories": ["Yellow/Mustard cushions", "Abstract art", "Glass decor"],
            "lighting": ["Crystal chandelier", "Warm floor lamp"],
            "wall": ["Dulux – Gooseberry", "Jotun – Lavender Touch"]
        },
        "Dark / Bold": {
            "message": "Dramatic and stylish.",
            "palette": [
                {"hex": "#F5F5DC", "name": "Beige"},
                {"hex": "#FFFFFF", "name": "Pure White"},
                {"hex": "#FF4500", "name": "Orange Pop"}
            ],
            "furniture": ["Dark grey sofa", "Black table", "Beige chair"],
            "accessories": ["Orange pillows", "Abstract art", "Gold frames"],
            "lighting": ["Strong LED", "Gold chandelier"],
            "wall": ["Jotun – Midnight", "Dulux – Charcoal"]
        }
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No image uploaded"})
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    rgb_list = get_dominant_colors(filepath)
    category, rec = classify_and_recommend(rgb_list)
    dominant_rgb = rgb_list[0] 
    return jsonify({
        "dominant_color_rgb": f"rgb{dominant_rgb}",
        "color_name": category,
        "message": rec["message"],
        "palette": rec["palette"], 
        "furniture": rec["furniture"],
        "accessories": rec["accessories"],
        "lighting": rec["lighting"],
        "wall": rec["wall"],
        "image_url": filepath
    })

if __name__ == "__main__":
    app.run(debug=True)