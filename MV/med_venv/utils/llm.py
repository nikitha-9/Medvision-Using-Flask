# utils/llm.py

def generate_response(symptoms: str, label: str) -> str:
    """
    Generate a medical suggestion based on symptoms and X-ray prediction label.
    """
    label = label.lower()
    suggestions = {
        "no finding": "The X-ray appears normal. If symptoms persist, consider further clinical evaluation.",
        "pneumonia": "The X-ray suggests pneumonia. Suggested treatment includes antibiotics, rest, and hydration. A follow-up chest X-ray may be required.",
        "cardiomegaly": "The X-ray shows signs of an enlarged heart. Further cardiac evaluation such as an echocardiogram is recommended.",
        "edema": "Signs of fluid buildup are present. Monitor respiratory status and consider diuretics as prescribed by a physician.",
        "atelectasis": "The lung may be partially collapsed. Suggested next steps include breathing exercises and physical therapy.",
        "consolidation": "The X-ray suggests lung consolidation. Antibiotic therapy and supportive care may be required.",
        "pleural effusion": "There appears to be fluid in the pleural space. Diagnostic thoracentesis or imaging guidance may be needed.",
        "infiltration": "Infiltrates detected may indicate infection or inflammation. Clinical correlation is essential.",
        "fibrosis": "Lung fibrosis is suspected. Consider referral to a pulmonologist for long-term management.",
        "tuberculosis": "Possible TB signs present. Initiate TB testing and notify health authorities if confirmed.",
    }

    # Get suggestion based on label
    suggestion = suggestions.get(label, "Abnormality detected. Further diagnostic tests and physician consultation are advised.")

    # Combine with symptom info if provided
    if symptoms.strip():
        return f"Based on the provided symptoms ({symptoms}) and the X-ray indicating {label}, here is a suggestion: {suggestion}"
    else:
        return f"The X-ray indicates {label}. {suggestion}"
