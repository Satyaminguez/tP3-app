"""Chatbot IA pour interroger les données."""
from litellm import completion
import pandas as pd


class DataAnalysisAssistant:
    def __init__(self, df: pd.DataFrame, model="ollama/mistral"):
        self.df = df
        self.model = model
        self.context = self._build_context()
        self.history = []
    
    def _build_context(self) -> str:
        return f"""
Tu es un assistant data analyst.

DATASET :
- Lignes : {len(self.df)}
- Colonnes : {list(self.df.columns)}
- Types : {self.df.dtypes.to_dict()}

Extrait :
{self.df.head(5).to_string()}

Réponds aux questions demandées de manière éducative, tout en restant simple, hormis si l'utilisateur te demande de rentrer dans le détail.
"""

    def analyze(self, question: str) -> str:
        messages = [{"role": "system", "content": self.context}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": question})

        response = completion(
            model=self.model,
            messages=messages,
            api_base="http://localhost:11434"
        )

        answer = response.choices[0].message.content

        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": answer})

        return answer
