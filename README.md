# Resume Tailor

> Paste a resume and job description. Get a prioritized match analysis.

## Live Demo
[Link here]

# What it does
Paste a resume and job description. Get a prioritized keyword/phrase match analysis.

## How It works
1. User pastes their resume
2. User pastes a job description
3. NLP extracts keywords and phrases
4. App highlights matched, missing, and ignored items

## 🎯The System Flow 
1. Extract keywords and phrases from resume and job description
2. Normalize and standardize them
3. Compare using exact and rule-based matching
4. Identify missing, matched, and extra elements
5. Score the alignment
6. Generate targeted suggestions for improvement


## Tech Stack
- Python + Flask
- spaCy (NLP extraction and filtering)
- OpenRouter API (planned future integration)

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
Then open `.env` and replace `your_key_here` with your actual OpenRouter API key.


### 6. Run the app
```bash
python app.py
```



## Environment Variables
OPENROUTER_API_KEY =your_key_here

## Author 
Issa Yaroo