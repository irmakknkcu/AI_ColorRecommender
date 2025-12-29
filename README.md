

```markdown
# AI Room Color Consultant

A modern and stylish room color analysis web application powered by Google Gemini AI. It analyzes room photos uploaded by users to detect dominant colors and offers suitable wall paint and decoration suggestions.

## Features

- **Image Upload:** Easy image upload via drag & drop or file selection.
- **AI-Powered Analysis:** Advanced color analysis with Google Gemini AI.
- **Color Palette:** Visual representation of detected dominant colors.
- **Detailed Recommendations:** Suggestions for wall paint, furniture, and decoration.
- **Responsive Design:** Mobile-friendly modern interface.
- **Fast and Secure:** Efficient image processing and API integration.

## Installation

### 1. Requirements

- Python 3.8 or higher
- Google Gemini API Key (You can obtain one via Google AI Studio)

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Set API Key

#### Option 1: Environment Variable (Recommended)

```bash
export GEMINI_API_KEY="your-api-key-here"

```

#### Option 2: Edit app.py

Replace the placeholder in the app.py file with your actual API key:

```python
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-actual-api-key-here')

```

### 4. Run the Application

```bash
python app.py

```

The application will run at http://localhost:8000.

## Usage

1. Navigate to http://localhost:8000 in your web browser.
2. Drag and drop your room photo or click the "Select File" button.
3. Click the "Analyze" button.
4. View the detailed AI analysis results and color suggestions.
5. Click on color codes to copy them to the clipboard.

## Project Structure

```
color/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── style.css          # Modern CSS styles
│   └── script.js          # Frontend JavaScript code
└── uploads/               # Uploaded images (automatically generated)

```

## Technologies

* **Backend:** Flask (Python)
* **AI:** Google Gemini 1.5 Flash
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Image Processing:** Pillow (PIL)

## API Endpoints

### GET /

View the homepage.

### POST /analyze

Analyze the room image.

**Request:**

* Content-Type: multipart/form-data
* Body: image (file)

**Response:**

```json
{
  "success": true,
  "analysis": "Detailed analysis text...",
  "dominant_colors": ["FF5733", "33FF57", "3357FF"],
  "image_base64": "data:image/png;base64,..."
}

```

## Security Notes

* Never commit your API key to Git.
* Use debug=False in production environments.
* The file size limit is 16MB.
* Only image file formats are accepted (PNG, JPG, JPEG, GIF, WEBP).

## License

This project is open source and free to use.

## Contributing

Feel free to send pull requests for suggestions and contributions!

```

```