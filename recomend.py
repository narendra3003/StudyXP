import google.generativeai as genai


genai.configure(api_key="AIzaSyBxwBtzmckhMSCi8iuDCi8eXaVPgg7Yrig")  

model = genai.GenerativeModel("gemini-1.5-pro")

# Fixed prompt
fixed_prompt = "Analyze my study performance based on patterns and give one-line recommendations."


def analyze_study_pattern(study_hours_per_day, mock_test_scores):
    if not study_hours_per_day or not mock_test_scores:
        return "Error: Study hours or mock test scores data is missing."

    if isinstance(study_hours_per_day, dict):
        study_hours_per_day = [study_hours_per_day[key] for key in sorted(study_hours_per_day.keys())]

    study_data = "\n".join([f"Day {i+1}: {study_hours_per_day[i]}" for i in range(len(study_hours_per_day))])
    mock_test_data = "\n".join([f"Mock Test {i+1}: {mock_test_scores[i]}" for i in range(len(mock_test_scores))])
    
    full_prompt = f"{fixed_prompt}\n\nStudy Hours Data:\n{study_data}\n\nMock Test Scores:\n{mock_test_data}\n\nAnalyze my study performance over the past week across all subjects and identify which subjects I should focus on more, based on study time, mock test scores, and consistency, give short 3 lines insights, remove bold or any styling just plain text. Analyzing it it should give a specific subject to be focused on more based on the data provided."
    
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"



study_hours_per_day = [
    [2, 3, 1],  # Day 1: Subject 1 → 2 hrs, Subject 2 → 3 hrs, Subject 3 → 1 hr
    [3, 2, 2],  # Day 2
    [1, 4, 3],   # Day 3
    [2, 4, 6],
    [5, 4, 5],
    [2, 4, 5],
    [3, 4, 4]
]


mock_test_scores = [
    [70, 80, 65],  # Day 1
    [75, 85, 60],  # Day 2
    [60, 90, 70],   # Day 3
    [70, 80,90],
    [75, 80, 76],
    [69, 87, 78],
    [76, 80, 80]
]


recommendation = analyze_study_pattern(study_hours_per_day, mock_test_scores)

print("\n *Gemini's Study Recommendation:*")
print(recommendation)