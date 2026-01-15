from datasets import Dataset
from ragas import evaluate
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)
from ragas.llms import llm_factory

from image_testset import image_eval_data
from text_testset import rag_test_data

# --------------------------------------------------
# Combine evaluation datasets
# --------------------------------------------------
dataset = Dataset.from_list(image_eval_data + rag_test_data)

# --------------------------------------------------
# OFFICIAL RAGAS Instructor LLM
# --------------------------------------------------
eval_llm = llm_factory("gpt-4o-mini")

# --------------------------------------------------
# Metrics (OFFICIALLY SUPPORTED)
# --------------------------------------------------
metrics = [
    Faithfulness(llm=eval_llm),
    AnswerRelevancy(llm=eval_llm),
    ContextPrecision(llm=eval_llm),
    ContextRecall(llm=eval_llm),
]

# --------------------------------------------------
# Run evaluation
# --------------------------------------------------
result = evaluate(
    dataset=dataset,
    metrics=metrics
)

print(result)
