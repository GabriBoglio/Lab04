class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand_assegnato = None

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        desc = f"[{self.codice}] {self.nome} {self.cognome}"
        if self.stand_assegnato:
            desc += f" -> Assegnato a: {self.stand_assegnato.codice}"
        else:
            desc += " -> Nessuno stand assegnato"
        return desc


class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def get_stato_str(self):
        return "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()
        return NotImplemented


class StandStandard(Stand):
    def __str__(self):
        return (f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - "
                f"Prezzo {self.calcola_prezzo():.2f}€ - {self.get_stato_str()}")


class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese = int(prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.prese)

    def __str__(self):
        return (f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - "
                f"Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.prese} - {self.get_stato_str()}")


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        return (f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} - "
                f"Prezzo {self.calcola_prezzo():.2f}€ - Posizione: {self.posizione} - {self.get_stato_str()}")


class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self.stands = []
        self.espositori = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        if isinstance(nuovo_nome, str) and nuovo_nome.strip():
            self._nome = nuovo_nome
        else:
            print("Errore: Il nome deve essere una stringa valida.")

    def carica_file_dati(self, file_path):
        try:
            with open(file