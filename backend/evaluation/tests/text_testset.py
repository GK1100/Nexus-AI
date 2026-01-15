from datasets import Dataset

rag_test_data = [
    {
        "question": "What is the main objective of the proposed framework?",
        "answer": "To accurately estimate password strength using lightweight machine learning models and provide real-time user feedback.",
        "contexts": [
            "Accurately estimating password strength is critical for improving user security and guiding real-time feedback during password creation.",
            "We present a two-stage machine-learning framework for password strength estimation."
        ],
        "response": "The main objective is to estimate password strength accurately using machine learning and provide real-time feedback to users."
    },
    {
        "question": "Which two machine learning models are used in the proposed system?",
        "answer": "Linear Regression and K-Nearest Neighbors (KNN).",
        "contexts": [
            "We apply both linear regression to predict a continuous strength score and k-nearest neighbors classification to categorize passwords."
        ],
        "response": "The system uses Linear Regression and K-Nearest Neighbors models."
    },
    {
        "question": "How many password samples were used after data cleaning?",
        "answer": "500 valid password entries.",
        "contexts": [
            "We loaded 507 rows from passwords.csv, then dropped seven blank rows and six duplicates, yielding N = 500 valid entries."
        ],
        "response": "After cleaning, 500 valid password samples were used."
    },
    {
        "question": "What are the six features extracted from each password?",
        "answer": "Length, lowercase count, uppercase count, digit count, special character count, and Shannon entropy.",
        "contexts": [
            "We extracted six numeric features: length, lowercase count, uppercase count, digit count, special character count, and Shannon entropy."
        ],
        "response": "The extracted features include length, lowercase, uppercase, digits, special characters, and Shannon entropy."
    },
    {
        "question": "What accuracy did the KNN classifier achieve?",
        "answer": "97% classification accuracy.",
        "contexts": [
            "The KNN classifier achieved 97% overall accuracy."
        ],
        "response": "The KNN classifier achieved an accuracy of 97 percent."
    },
    {
        "question": "Which password class showed the strongest recall performance?",
        "answer": "The Strong password class.",
        "contexts": [
            "Strong: precision = 0.97, recall = 1.00 (96/96 correctly identified)."
        ],
        "response": "The Strong password class showed the highest recall performance."
    },
    {
        "question": "Where did most classification errors occur?",
        "answer": "Within the Medium password category.",
        "contexts": [
            "Misclassifications occurred only within the Medium category."
        ],
        "response": "Most classification errors occurred in the Medium category."
    },
    {
        "question": "Why is linear regression able to achieve near-zero error in this study?",
        "answer": "Because the target strength score was a deterministic weighted sum of the extracted features.",
        "contexts": [
            "The regression simply inverted the weighted sum by design, resulting in near-zero MAE and MSE."
        ],
        "response": "Linear regression achieved near-zero error because the target score was a deterministic function of the features."
    },
    {
        "question": "What tool was used to deploy the interactive password strength estimator?",
        "answer": "Gradio.",
        "contexts": [
            "We wrapped the regression predictor in a Gradio web interface for interactive demonstration."
        ],
        "response": "The system was deployed using a Gradio web interface."
    },
    {
        "question": "What is a key advantage of the proposed approach over deep learning models?",
        "answer": "It requires minimal data, no GPUs, and enables real-time client-side feedback.",
        "contexts": [
            "Unlike deep models, it functions without dictionaries or GPU-intensive processes, making it suitable for instantaneous feedback."
        ],
        "response": "A key advantage is that it works without GPUs or large datasets and supports real-time feedback."
    }
]

dataset = Dataset.from_list(rag_test_data)
