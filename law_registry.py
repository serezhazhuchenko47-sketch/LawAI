import json
import os
from difflib import get_close_matches


class LawRegistry:

    def __init__(self):

        self.index = {}

        if os.path.exists("laws_index.json"):

            with open(
                "laws_index.json",
                "r",
                encoding="utf-8"
            ) as f:

                self.index = json.load(f)

    def find(self, law_name: str):

        law_name = law_name.lower().strip()

        # Точний збіг

        if law_name in self.index:

            return self.index[law_name]

        # Частковий збіг

        for title, law_id in self.index.items():

            if law_name in title:

                return law_id

        # Пошук схожої назви

        matches = get_close_matches(
            law_name,
            self.index.keys(),
            n=1,
            cutoff=0.6
        )

        if matches:

            return self.index[matches[0]]

        return None


registry = LawRegistry()