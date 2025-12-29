import os
from flask import Flask, render_template, request, jsonify
import google.genai as genai
from PIL import Image
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.urandom(24)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
client = genai.Client(api_key=GEMINI_API_KEY)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_room():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Please upload an image'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Please upload PNG, JPG, JPEG, GIF or WEBP'}), 400
        
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Prompt for Google Gemini - Request JSON format response
        prompt = """Analyze this room photo and provide your response ONLY in JSON format. Do not add any other text.

Response format:
{
  "dominant_colors": [
    {"hex": "#HEXCODE1", "name": "Color Name", "percentage": 30, "description": "Where this color appears in the room"},
    {"hex": "#HEXCODE2", "name": "Color Name", "percentage": 25, "description": "Description"},
    {"hex": "#HEXCODE3", "name": "Color Name", "percentage": 20, "description": "Description"}
  ],
  "wall_colors": [
    {"hex": "#HEXCODE", "name": "Color Name", "reason": "Detailed explanation of why this color is suitable"},
    {"hex": "#HEXCODE", "name": "Color Name", "reason": "Explanation"}
  ],
  "furniture_colors": ["Recommended furniture color description 1", "Description 2"],
  "accessories_colors": ["Recommended accessory color description 1", "Description 2"],
  "decoration_tips": ["Decoration tip 1", "Tip 2", "Tip 3"],
  "color_harmony": "Color combinations that harmonize with existing colors and contrast explanation",
  "summary": "Summary of the overall color palette and decoration recommendations for the room"
}

RULES:
1. Response must be ONLY valid JSON, NO other text before or after
2. Hex codes must start with # and be exactly 6 characters (e.g., #FF5733)
3. All text must be in English
4. Identify at least 3-5 dominant colors
5. Provide at least 3-5 wall color suggestions
6. Write detailed and descriptive text for each recommendation"""
        
        # Prepare image (as PIL Image)
        image_pil = Image.open(io.BytesIO(image_bytes))
        
        # Analyze using Gemini model
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=[prompt, image_pil]
        )
        
        analysis_text = response.text
        
        # Try to parse JSON
        import json
        import re
        
        parsed_data = None
        
        # First extract JSON from ```json or ``` code blocks
        json_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', analysis_text)
        if json_block_match:
            try:
                json_str = json_block_match.group(1)
                parsed_data = json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # If no code block, search for direct JSON
        if not parsed_data:
            json_match = re.search(r'\{[\s\S]*\}', analysis_text)
            if json_match:
                try:
                    json_str = json_match.group(0)
                    json_str = json_str.strip()
                    parsed_data = json.loads(json_str)
                except json.JSONDecodeError:
                    # Last resort: get only the first JSON object
                    try:
                        brace_count = 0
                        start_idx = json_str.find('{')
                        end_idx = start_idx
                        for i, char in enumerate(json_str[start_idx:], start_idx):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    end_idx = i + 1
                                    break
                        if end_idx > start_idx:
                            parsed_data = json.loads(json_str[start_idx:end_idx])
                    except:
                        parsed_data = None
        
        # Extract hex color codes (fallback)
        hex_colors = []
        if parsed_data and 'dominant_colors' in parsed_data:
            hex_colors = [color['hex'].replace('#', '') for color in parsed_data['dominant_colors'] if 'hex' in color]
        else:
            hex_colors = re.findall(r'#([A-Fa-f0-9]{6})', analysis_text)
        
        # Format response
        result = {
            'success': True,
            'analysis': analysis_text,
            'parsed_data': parsed_data,
            'dominant_colors': hex_colors[:5] if hex_colors else [],
            'image_base64': f"data:image/png;base64,{img_base64}"
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
