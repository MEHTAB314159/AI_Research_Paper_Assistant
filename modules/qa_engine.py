import torch

from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering
)

from config import QA_MODEL


class QAEngine:

    def __init__(self):

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                QA_MODEL
            )
        )

        self.model = (
            AutoModelForQuestionAnswering
            .from_pretrained(QA_MODEL)
        )

        self.model.eval()

    def answer(
        self,
        question,
        contexts
    ):

        best_answer = None

        for item in contexts:

            context = item["text"]

            inputs = self.tokenizer(
                question,
                context,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )

            with torch.no_grad():

                outputs = self.model(
                    **inputs
                )

            start_index = torch.argmax(
                outputs.start_logits
            )

            end_index = torch.argmax(
                outputs.end_logits
            )

            if end_index < start_index:

                continue

            answer_tokens = (
                inputs.input_ids[
                    0,
                    start_index:end_index + 1
                ]
            )

            answer = self.tokenizer.decode(
                answer_tokens,
                skip_special_tokens=True
            )

            start_score = torch.max(
                outputs.start_logits
            ).item()

            end_score = torch.max(
                outputs.end_logits
            ).item()

            score = (
                start_score +
                end_score
            ) / 2

            result = {
                "answer": answer,
                "score": score,
                "source": item["source"],
                "page": item["page"]
            }

            if (
                best_answer is None
                or result["score"] >
                best_answer["score"]
            ):

                best_answer = result

        return best_answer