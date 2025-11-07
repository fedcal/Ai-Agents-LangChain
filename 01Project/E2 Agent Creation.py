# In questo esercizio, creerai la struttura di base di un agente di intelligenza artificiale in grado di elaborare gli input dell'utente e generare risposte utilizzando un modello linguistico. Questo è il primo passo nella progettazione di un agente interattivo e ti concentrerai sulla definizione dei suoi componenti essenziali.
#
# Obiettivo
#
# Il tuo compito è implementare un agente che possa:
#
# - Essere inizializzato con impostazioni configurabili, inclusi nome, ruolo, istruzioni e parametri del modello.
# - Inviare messaggi utente a un modello linguistico, assicurandosi che la risposta sia allineata con il ruolo e le istruzioni specificati.
# - Restituire la risposta generata dall'intelligenza artificiale come stringa.
#
# Passaggi
#
# - Creare un costruttore che consenta la personalizzazione del nome, del ruolo e delle istruzioni dell'agente.
# - Assicurarsi che l'agente interagisca con un modello linguistico, passando il messaggio utente insieme alle istruzioni di sistema.
# - Implementare un metodo per gestire l'elaborazione dei messaggi, assicurandosi che la risposta venga recuperata correttamente.

from openai import OpenAI
from dotenv import load_dotenv

# Carica le variabili d'ambiente (ad esempio la chiave API OpenAI)
load_dotenv()


# Considerazioni
#
# - Il ruolo e le istruzioni dovrebbero guidare il comportamento dell'agente nella generazione delle risposte. - I parametri del modello (come la temperatura) devono essere configurabili.
# - Assicurarsi che l'agente mantenga la semplicità fornendo al contempo una risposta strutturata.
#
# Costruttore
#
# Innanzitutto, creare una classe chiamata Agent con i seguenti parametri nel metodo `__init__`:
# - nome (predefinito: "Agente")
# - ruolo (predefinito: "Assistente personale")
# - istruzioni (predefinito: "Aiuta gli utenti con qualsiasi domanda")
# - modello (predefinito: "gpt-4o-mini")
# - temperatura (predefinita: 0.0)
#
# Si consiglia di rendere il client accessibile all'interno dell'agente.
#
# Invoke
#
# La maggior parte dei framework di agentic fornisce un metodo `invoke()`. Per motivi di compatibilità, faremo lo stesso. Questo metodo dovrebbe:
# - accettare un messaggio come input;
# - inviare il messaggio all'API dell'LLM utilizzando il modello e la temperatura specificati;
# - formattare la richiesta API con il ruolo di sistema e l'input dell'utente;
# - restituire la risposta dell'LLM.
#
# Nota che il prompt di sistema deve tenere conto del ruolo e delle istruzioni, altrimenti non si comporterà come desiderato.

class Agente:
    """
    Classe che rappresenta un agente AI semplice e personalizzabile.
    Permette di interagire con un modello linguistico OpenAI.
    """

    def __init__(
        self,
        nome: str = "Agente",
        ruolo: str = "Assistente Personale",
        istruzioni: str = "Aiuta gli utenti con qualsiasi domanda",
        modello: str = "gpt-4o-mini",
        temperatura: float = 0.0,
    ):
        """
        Inizializza l'agente con parametri personalizzabili.
        - nome: nome dell'agente
        - ruolo: ruolo dell'agente (es. Assistente, Tutor, Narratore)
        - istruzioni: istruzioni specifiche per il comportamento dell'agente
        - modello: modello OpenAI da utilizzare
        - temperatura: creatività delle risposte (0 = deterministico, 1 = creativo)
        """
        self.nome = nome
        self.ruolo = ruolo
        self.istruzioni = istruzioni
        self.modello = modello
        self.temperatura = temperatura
        self.client = OpenAI()

    def invoca(self, messaggio: str) -> str:
        """
        Invia un messaggio all'LLM e restituisce la risposta generata.
        - messaggio: domanda o richiesta dell'utente
        """
        risposta = self.client.chat.completions.create(
            model=self.modello,
            temperature=self.temperatura,
            messages=[
                {
                    "role": "system",
                    "content": f"Sei un agente AI, il tuo ruolo è {self.ruolo}, e devi {self.istruzioni}",
                },
                {
                    "role": "user",
                    "content": messaggio,
                }
            ]
        )
        return risposta.choices[0].message.content

# Se il file viene eseguito direttamente, vengono creati e testati diversi agenti
if __name__ == '__main__':
    # Agente di default
    agente = Agente()
    risposta_default = agente.invoca("Qual è la capitale della Francia?")
    print("Ruolo agente:", agente.ruolo)
    print("Risposta agente di default:", risposta_default)

    # Agente Viaggi
    agente_viaggi = Agente(
        ruolo="Assistente Viaggi",
        istruzioni="Fornisci raccomandazioni di viaggio.",
        temperatura=0.7
    )
    risposta_viaggi = agente_viaggi.invoca("Dove posso andare in vacanza a dicembre?")
    print("\nRuolo agente:", agente_viaggi.ruolo)
    print("Risposta agente viaggi:", risposta_viaggi)

    # Agente Tutor di Matematica
    agente_matematica = Agente(
        ruolo="Tutor di Matematica",
        istruzioni="Aiuta gli studenti a risolvere problemi di matematica passo-passo."
    )
    risposta_matematica = agente_matematica.invoca("Come si risolve un'equazione quadratica?")
    print("\nRuolo agente:", agente_matematica.ruolo)
    print("Risposta agente matematica:", risposta_matematica)

    # Agente Storyteller
    agente_storie = Agente(
        ruolo="Narratore",
        istruzioni="Crea storie fantasiose.",
        temperatura=0.9
    )
    risposta_storie = agente_storie.invoca("Raccontami una storia su un drago e un mago.")
    print("\nRuolo agente:", agente_storie.ruolo)
    print("Risposta agente storyteller:", risposta_storie)
