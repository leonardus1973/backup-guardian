# Contribuire a Backup Guardian

Prima di tutto, grazie per aver considerato di contribuire a Backup Guardian! 🎉

## Come Contribuire

### Segnalare Bug 🐛

Se trovi un bug, apri un [Issue](https://github.com/leonardus1973/backup-guardian/issues) includendo:

- Descrizione chiara del problema
- Passi per riprodurre il bug
- Comportamento atteso vs comportamento effettivo
- Versione di Home Assistant
- Versione di Backup Guardian
- Log rilevanti (se disponibili)

### Proporre Nuove Funzionalità 💡

Per proporre una nuova funzionalità:

1. Controlla che non sia già stata proposta negli [Issues](https://github.com/leonardus1973/backup-guardian/issues)
2. Apri un nuovo Issue con tag `enhancement`
3. Descrivi dettagliatamente la funzionalità
4. Spiega perché sarebbe utile

### Pull Request

1. **Fork** il repository
2. Crea un **branch** per la tua modifica:
   ```bash
   git checkout -b feature/nome-funzionalità
   ```
3. Fai le tue modifiche seguendo gli standard di codice
4. **Testa** le modifiche su una installazione locale di Home Assistant
5. **Commit** con messaggi chiari:
   ```bash
   git commit -m "Add: descrizione breve della modifica"
   ```
6. **Push** sul tuo fork:
   ```bash
   git push origin feature/nome-funzionalità
   ```
7. Apri una **Pull Request** verso il branch `main`

### Standard di Codice

- Usa **4 spazi** per l'indentazione (no tab)
- Segui le convenzioni [PEP 8](https://pep8.org/) per Python
- Commenta il codice quando necessario
- Mantieni le funzioni brevi e focalizzate
- Usa nomi di variabili descrittivi

### Struttura del Progetto

```
backup_guardian/
├── custom_components/
│   └── backup_guardian/
│       ├── __init__.py          # Inizializzazione integrazione
│       ├── config_flow.py       # Configurazione UI
│       ├── const.py             # Costanti
│       ├── coordinator.py       # Gestione dati
│       ├── sensor.py            # Sensori
│       ├── manifest.json        # Metadati integrazione
│       ├── strings.json         # Traduzioni base
│       ├── translations/        # Traduzioni localizzate
│       │   └── it.json
│       └── www/                 # Risorse frontend
│           └── backup-guardian-card.js
├── README.md
├── GUIDA_RAPIDA.md
├── CHANGELOG.md
├── LICENSE
└── hacs.json
```

### Testing

Prima di inviare una PR, assicurati di:

1. Testare su una installazione reale di Home Assistant
2. Verificare che tutti i sensori funzionino correttamente
3. Controllare che la card Lovelace si visualizzi correttamente
4. Verificare che non ci siano errori nei log

### Processo di Review

1. Un maintainer revisionerà la tua PR
2. Potrebbero essere richieste modifiche
3. Una volta approvata, la PR verrà unita al branch main
4. Le modifiche saranno incluse nella prossima release

### Aree che Necessitano Contributi

- 🌐 **Traduzioni**: Traduzioni in altre lingue
- 📊 **Grafici**: Implementazione grafici storici
- 🔌 **Integrazioni**: Supporto Google Drive, Dropbox, ecc.
- 📱 **UI/UX**: Miglioramenti alla card Lovelace
- 📝 **Documentazione**: Esempi, tutorial, guide
- 🧪 **Testing**: Unit test, integration test

### Domande?

Se hai domande:

- Apri un [Discussion](https://github.com/leonardus1973/backup-guardian/discussions)
- Contatta via Issue

## Codice di Condotta

### Il Nostro Impegno

Ci impegniamo a rendere la partecipazione al nostro progetto un'esperienza libera da molestie per tutti, indipendentemente da età, dimensioni del corpo, disabilità, etnia, identità ed espressione di genere, livello di esperienza, nazionalità, aspetto personale, razza, religione o identità e orientamento sessuale.

### Standard

Esempi di comportamento che contribuiscono a creare un ambiente positivo:

- Usare un linguaggio accogliente e inclusivo
- Rispettare punti di vista ed esperienze diverse
- Accettare con grazia le critiche costruttive
- Concentrarsi su ciò che è meglio per la comunità
- Mostrare empatia verso gli altri membri della comunità

Comportamenti inaccettabili:

- Linguaggio o immagini sessualizzati
- Trolling, commenti offensivi/dispregiativi
- Molestie pubbliche o private
- Pubblicare informazioni private altrui senza permesso
- Altre condotte che potrebbero essere ragionevolmente considerate inappropriate

### Grazie! 🙏

Il tuo contributo è apprezzato e aiuta a rendere Backup Guardian migliore per tutti!

---

**Happy Coding! 🚀**
