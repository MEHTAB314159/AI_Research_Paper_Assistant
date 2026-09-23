import spacy


class NEREngine:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract_entities(self, text):

        document = self.nlp(text)

        entities = []

        for entity in document.ents:

            entities.append({
                "text": entity.text,
                "label": entity.label_
            })

        return entities