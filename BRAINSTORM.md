## Input → Process → Extract → Compare → Detect Gaps

- User provide 2 inputs (RESUME + JOB_DESC)
- Extract the keywords from the inputs (Skills + Tools + Roles + Concepts)
- Clean the extracted key words and filter appropriately 
- Separate keywords from phrases (Python, Rest-Api) before tokenization happens
- Resume matching vs Job matching (what does the job has that resume does not have) - finding the missing keyword and phrases
- Highlight resume extra skills not required in the job but cool.
- AI resume rewriting (missing_keywords + missing_phrases)
