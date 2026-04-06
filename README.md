# Resume Tailor

> Paste a job description. Get a tailored resume. Download as PDF

## Live Demo
[Link here]

# What it does
Paste a job description. Get a tailored resume. Download as PDF

## How It works
1. User pastes their resume
2. User pastes a job description
3. AI rewrites resume bullets to match the job
4. User downloads a styled PDF

## Tech Stack
- Python + Flask
- OpenRouter API (AI rewriting)
- WeasyPrint (PDF generation)

## Run Locally
Step by step instruction here

### Prerequisites
- Python 3.10 or higher installed on your machine
- An openRouter API key — get one at [openrouter.ai](https://openrouter.ai/)


### 1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-tailor.git
cd resume-tailor
```
### 2. Create a virtual environment
```bash
python -m venv venv
```
### 3. Activate the virtual environment

**Mac/Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your environment variables
```bash
cp .env.example .env
```
Then open `.env` and replace `your_key_here` with your actual Anthropic API key.


### 6. Run the app
```bash
python app.py
```



## Environment Variables
OPENROUTER_API_KEY =your_key_here

## Author 
Issa Yaroo