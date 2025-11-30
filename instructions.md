## Overview

A modern Python Flask web application that uses the Groq API to summarize text content from uploaded TXT files. The application provides a clean, user-friendly interface for uploading documents, viewing original content, and displaying AI-generated summaries in a well-formatted manner.

## Features

- **File Upload**: Simple drag-and-drop or file picker interface for uploading TXT files
- **Content Display**: View the original uploaded text content
- **AI Summarization**: Generate concise summaries using the Groq API
- **Clean UI**: Modern, responsive design with clear separation of content areas
- **Error Handling**: User-friendly error messages for invalid files or API issues

## Core Functions

The application provides three main functional areas:

1. **File Upload Section**: A dedicated area for users to upload TXT files with clear visual feedback
2. **Original Content Display**: A readable section showing the full uploaded text content
3. **Summary Output**: A clean, formatted area displaying the AI-generated summary of the uploaded content

## Technical Stack

- **Backend**: Python 3.8+ with Flask framework
- **Frontend**: HTML5, CSS3, JavaScript (vanilla or minimal framework)
- **API Integration**: Groq API for text summarization
- **File Handling**: Python's built-in file I/O for processing uploaded files

## Project Structure

```
CapstoneProject/
├── app.py                 # Main Flask application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── instructions.md       # This file
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── main.js       # Client-side JavaScript
└── templates/            # Flask HTML templates
    └── index.html       # Main application page
```

## Prerequisites

Before setting up the project, ensure you have:

- Python 3.8 or higher installed
- pip (Python package manager)
- A Groq API key ([Get one here](https://console.groq.com/))
- A code editor (VS Code, PyCharm, etc.)

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd CapstoneProject
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install flask python-dotenv groq
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important**: Never commit the `.env` file to version control. Ensure it's listed in `.gitignore`.

### 5. Run the Application

```bash
python app.py
```

Or if using Flask's development server:

```bash
flask run
```

The application will be available at `http://localhost:5000` (or the port specified in your configuration).

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Click the upload area or use the file picker to select a TXT file
3. View the original content in the display area
4. Click the "Summarize" button to generate a summary
5. View the summarized output in the results section

## API Configuration

### Groq API Setup

1. Sign up for a Groq account at [console.groq.com](https://console.groq.com/)
2. Navigate to API Keys section
3. Generate a new API key
4. Add the key to your `.env` file as `GROQ_API_KEY`

### API Usage Notes

- Ensure you have sufficient API credits/quota
- Implement rate limiting if processing multiple files
- Handle API errors gracefully (network issues, rate limits, etc.)

## Development Notes

- Use Flask's built-in development server for local development
- For production, use a production WSGI server like Gunicorn
- Implement proper error handling and validation for file uploads
- Consider adding file size limits to prevent abuse
- Add loading indicators during API calls for better UX

## Troubleshooting

**Issue**: Module not found errors

- **Solution**: Ensure virtual environment is activated and dependencies are installed

**Issue**: API key errors

- **Solution**: Verify `.env` file exists and contains the correct `GROQ_API_KEY`

**Issue**: File upload not working

- **Solution**: Check Flask's `MAX_CONTENT_LENGTH` configuration and file permissions

**Issue**: Port already in use

- **Solution**: Change the port in `app.py` or kill the process using the port

## Future Enhancements

- Support for multiple file formats (PDF, DOCX, etc.)
- Batch processing of multiple files
- Customizable summary length/format
- Export summaries to various formats
- User authentication and history
- Advanced text analysis features
