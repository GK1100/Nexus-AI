from datasets import Dataset

image_eval_data = [
    {
        "question": "What is the starting input shown in the pipeline diagram?",
        "answer": "Raw password strings.",
        "contexts": [
            "The top box in the diagram is labeled 'Raw Password Strings'."
        ],
        "response": "The pipeline starts with raw password strings."
    },
    {
        "question": "Which features are extracted from passwords according to the diagram?",
        "answer": "Length, lowercase, uppercase, digits, special characters, and entropy.",
        "contexts": [
            "The feature extraction box lists length, lowercase, uppercase, digits, special, and entropy."
        ],
        "response": "The diagram shows that length, lowercase, uppercase, digits, special characters, and entropy are extracted."
    },
    {
        "question": "What preprocessing step is applied before splitting the data?",
        "answer": "Standardization.",
        "contexts": [
            "After feature extraction, the next box in the pipeline is labeled 'Standardization'."
        ],
        "response": "Standardization is applied before the train-test split."
    },
    {
        "question": "Which two models are trained after the train-test split?",
        "answer": "Linear Regression and K-Nearest Neighbors (KNN) classifier.",
        "contexts": [
            "The pipeline branches after train-test split into Linear Regression and KNN Classifier."
        ],
        "response": "The models trained are Linear Regression and KNN Classifier."
    },
    {
        "question": "What outputs are produced by the two branches of the pipeline?",
        "answer": "A continuous strength score and categorical labels (Weak, Medium, Strong).",
        "contexts": [
            "Linear Regression outputs a continuous strength score and KNN outputs Weak, Medium, Strong."
        ],
        "response": "The outputs are a continuous strength score and password categories such as Weak, Medium, and Strong."
    }
]

image_dataset = Dataset.from_list(image_eval_data)
