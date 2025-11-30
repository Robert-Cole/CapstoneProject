from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from groq import Groq
import tempfile

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize Groq client
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    # Try loading from .env file directly as fallback (handles BOM)
    try:
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        with open(env_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'GROQ_API_KEY':
                        groq_api_key = value.strip()
                        os.environ['GROQ_API_KEY'] = groq_api_key  # Set it for later use
                        break
    except Exception as e:
        print(f"Warning: Could not read .env file: {e}")
    
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

client = Groq(api_key=groq_api_key)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and return file content"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only TXT files are allowed.'}), 400
        
        # Read file content
        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return jsonify({'error': 'File encoding error. Please ensure the file is UTF-8 encoded.'}), 400
        
        if not content.strip():
            return jsonify({'error': 'File is empty'}), 400
        
        return jsonify({
            'success': True,
            'content': content,
            'filename': secure_filename(file.filename)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    """Generate summary using Groq API"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'No content provided'}), 400
        
        content = data['content']
        
        if not content.strip():
            return jsonify({'error': 'Content is empty'}), 400
        
        # Truncate content if too long (Groq has token limits)
        max_length = 50000  # Approximate character limit
        if len(content) > max_length:
            content = content[:max_length] + "\n\n[Content truncated due to length...]"
        
        # Create prompt for summarization
        prompt = f"""Please provide a clear and concise summary of the following text. 
Focus on the main points, key ideas, and important information. 
Keep the summary well-structured and easy to read.

Text to summarize:
{content}"""
        
        # Call Groq API
        # Try multiple models in order of preference
        models_to_try = [
            "llama-3.3-70b-versatile",  # Latest versatile model
            "llama-3.1-8b-instant",     # Fast and reliable fallback
            "mixtral-8x7b-32768"         # Alternative high-quality model
        ]
        
        try:
            chat_completion = None
            for model_name in models_to_try:
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful assistant that provides clear, concise, and well-structured summaries of text content."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        model=model_name,
                        temperature=0.3,
                        max_tokens=2000
                    )
                    # If successful, break out of the loop
                    break
                except Exception as model_error:
                    # If this is the last model, re-raise the error
                    if model_name == models_to_try[-1]:
                        raise model_error
                    # Otherwise, try the next model
                    continue
            
            # Extract summary from successful API call
            if chat_completion:
                summary = chat_completion.choices[0].message.content
                
                return jsonify({
                    'success': True,
                    'summary': summary
                })
            else:
                raise Exception("Failed to get response from any model")
        
        except Exception as api_error:
            error_msg = str(api_error)
            if 'rate limit' in error_msg.lower():
                return jsonify({'error': 'API rate limit exceeded. Please try again later.'}), 429
            elif 'authentication' in error_msg.lower() or 'api key' in error_msg.lower():
                return jsonify({'error': 'API authentication failed. Please check your API key.'}), 401
            else:
                return jsonify({'error': f'API error: {error_msg}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

