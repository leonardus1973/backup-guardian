# 🛡️ Backup Guardian - Custom Integration per Home Assistant

**Backup Guardian** è una custom integration per Home Assistant OS che monitora i backup del Supervisor, mostrando informazioni dettagliate come nome, data, ora, dimensione e hash SHA256 di verifica.

![Version](https://img.shields.io/github/v/release/leonardus1973/backup-guardian)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.1+-blue)
![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)


## ✨ Caratteristiche

- 📊 **Monitoraggio completo** dei backup tramite Supervisor API
- 🔍 **Hash SHA256** per identificazione univoca di ogni backup
- 📈 **3 Sensori dedicati**:
  - Ultimo backup effettuato
  - Totale backup disponibili
  - Dimensione totale occupata
- 🎨 **Lovelace Card personalizzata** con interfaccia moderna e intuitiva
- 🔄 **Aggiornamento automatico** ogni 5 minuti
- 🚀 **Compatibile con HACS**
- 🌍 **Interfaccia in italiano**

## 📸 Screenshot

La card mostra:
- 📦 Ultimo backup con tutti i dettagli (nome, data, ora, dimensione, hash)
- 📊 Statistiche: totale backup e spazio occupato
- 🔘 Lista espandibile di tutti i backup
- 🎨 Design moderno che si integra con il tema di Home Assistant

## 📦 Installazione

### Metodo 1: HACS (Consigliato)

1. Apri **HACS** in Home Assistant
2. Vai su **Integrazioni**
3. Clicca sui **tre puntini** in alto a destra → **Repository personalizzati**
4. Aggiungi l'URL: `https://github.com/leonardus1973/backup-guardian`
5. Seleziona la categoria: **Integration**
6. Cerca "Backup Guardian" e clicca su **Scarica**
7. **Riavvia Home Assistant**

### Metodo 2: Installazione Manuale

1. Scarica l'ultima release da [GitHub Releases](https://github.com/leonardus1973/backup-guardian/releases)
2. Estrai il file ZIP
3. Copia la cartella `custom_components/backup_guardian` nella directory `config/custom_components/` di Home Assistant
4. La struttura deve essere: `config/custom_components/backup_guardian/`
5. **Riavvia Home Assistant**

## ⚙️ Configurazione

### Passo 1: Aggiungi l'Integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Clicca su **+ Aggiungi Integrazione**
3. Cerca "**Backup Guardian**"
4. Clicca sull'integrazione quando appare
5. Clicca su **Invia** per completare la configurazione

✅ L'integrazione è ora attiva! I sensori verranno creati automaticamente.

### Passo 2: Configura la Lovelace Card

#### A. Registra la Risorsa JavaScript

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Clicca su **+ Aggiungi risorsa**
3. Inserisci i seguenti dati:

**Se hai installato via HACS:**
- **URL**: `/hacsfiles/backup_guardian/backup-guardian-card.js`
- **Tipo di risorsa**: **Modulo JavaScript**

**Se hai installato manualmente:**
- **URL**: `/local/community/backup_guardian/backup-guardian-card.js`
- **Tipo di risorsa**: **Modulo JavaScript**

4. Clicca **Crea**

**IMPORTANTE**: Dopo aver aggiunto la risorsa:
- **Riavvia Home Assistant** (consigliato)
- **Svuota la cache del browser**: Ctrl+Shift+R (Windows/Linux) o Cmd+Shift+R (Mac)
- Se la card non appare, prova a usare una **finestra in incognito** per verificare che il problema sia la cache

#### B. Aggiungi la Card alla Dashboard

1. Apri una dashboard e clicca sui **tre puntini** → **Modifica dashboard**
2. Clicca su **+ Aggiungi Card**
3. Scorri in basso e seleziona **Manuale**
4. Incolla questa configurazione:

```yaml
type: custom:backup-guardian-card
entity: sensor.backup_guardian_totale_backup
last_backup_entity: sensor.backup_guardian_ultimo_backup
size_entity: sensor.backup_guardian_dimensione_totale
```

5. Clicca **Salva**
6. Clicca **Fine** per uscire dalla modalità modifica

✅ La card dovrebbe ora essere visibile!

## 📊 Sensori Disponibili

L'integrazione crea automaticamente **3 sensori** sotto il dispositivo "Backup Guardian":

### 1. `sensor.backup_guardian_ultimo_backup`
Mostra la data e ora dell'ultimo backup effettuato.

**Attributi:**
- `backup_name`: Nome del backup
- `backup_date`: Data in formato YYYY-MM-DD
- `backup_time`: Ora in formato HH:MM:SS
- `backup_size`: Dimensione in MB
- `backup_hash`: Hash SHA256 univoco per identificazione
- `backup_type`: Tipo di backup (full/partial)

### 2. `sensor.backup_guardian_totale_backup`
Indica il numero totale di backup presenti nel sistema.

**Attributi:**
- `backup_list`: Array con la lista completa di tutti i backup, ognuno con:
  - `name`: Nome del backup
  - `date`: Data
  - `time`: Ora
  - `size`: Dimensione
  - `hash`: Hash SHA256

### 3. `sensor.backup_guardian_dimensione_totale`
Mostra lo spazio totale occupato da tutti i backup in MB.

## 🎨 Funzionalità della Card

La card personalizzata offre:

- **Sezione Ultimo Backup**: Visualizza i dettagli completi dell'ultimo backup effettuato
- **Box Statistiche**: Due box affiancati con:
  - Numero totale di backup
  - Dimensione totale in MB
- **Bottone Espandibile**: Clicca su "Mostra Tutti i Backup" per vedere la lista completa
- **Lista Dettagliata**: Ogni backup mostra nome, data/ora, dimensione e hash
- **Design Responsive**: Si adatta automaticamente al tema di Home Assistant

## 🔧 Configurazione Avanzata

### Modifica Intervallo di Aggiornamento

Se vuoi modificare la frequenza di aggiornamento dei sensori (default: 5 minuti):

1. Modifica il file `custom_components/backup_guardian/const.py`
2. Cambia il valore di `UPDATE_INTERVAL`:

```python
UPDATE_INTERVAL = 300  # Secondi (300 = 5 minuti)
```

3. Riavvia Home Assistant

### Esempio di Automazione: Notifica Backup Mancante

```yaml
automation:
  - alias: "Avviso Backup Mancante"
    description: "Notifica se non viene effettuato un backup da più di 7 giorni"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: >
          {{ (now() - states.sensor.backup_guardian_ultimo_backup.last_changed).days > 7 }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Attenzione Backup"
          message: "Nessun backup effettuato da più di 7 giorni!"
```

### Esempio di Automazione: Notifica Nuovo Backup

```yaml
automation:
  - alias: "Notifica Nuovo Backup"
    description: "Invia una notifica quando viene completato un nuovo backup"
    trigger:
      - platform: state
        entity_id: sensor.backup_guardian_ultimo_backup
    action:
      - service: notify.mobile_app
        data:
          title: "✅ Backup Completato"
          message: >
            Nuovo backup: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_name') }}
            Dimensione: {{ state_attr('sensor.backup_guardian_ultimo_backup', 'backup_size') }}
```

## 🐛 Risoluzione Problemi

### I sensori non vengono creati

**Soluzione:**
1. Verifica di essere su **Home Assistant OS** o **Home Assistant Supervised**
2. Vai su **Impostazioni** → **Sistema** → **Log** e cerca errori relativi a `backup_guardian`
3. Verifica che l'integrazione sia attiva in **Dispositivi e Servizi**
4. Riavvia Home Assistant

### La card mostra "Custom element doesn't exist"

**Soluzione:**
1. Verifica che la risorsa JavaScript sia registrata correttamente in **Dashboard** → **Risorse**
2. Controlla che l'URL sia corretto:
   - HACS: `/hacsfiles/backup_guardian/backup-guardian-card.js`
   - Manuale: `/local/community/backup_guardian/backup-guardian-card.js`
3. **Svuota completamente la cache** del browser:
   - **Chrome/Edge**: Ctrl+Shift+Delete → "Immagini e file memorizzati" → Cancella
   - **Firefox**: Ctrl+Shift+Delete → "Cache" → Cancella
4. **Chiudi e riapri** completamente il browser
5. Prova in **modalità incognito** per escludere problemi di cache
6. Se ancora non funziona, riavvia Home Assistant

### La card non appare nella lista

**Soluzione:**
1. Verifica che il file esista in `/config/www/community/backup_guardian/backup-guardian-card.js`
2. Se installato via HACS, verifica che HACS abbia copiato il file correttamente
3. Svuota la cache del browser (Ctrl+Shift+R)
4. Riavvia Home Assistant

### Le dimensioni dei backup sono a 0 MB

**Soluzione:**
1. Controlla i log per errori nell'accesso all'API del Supervisor
2. Verifica che ci siano backup effettivi nel sistema
3. Riavvia l'integrazione: **Dispositivi e Servizi** → Backup Guardian → **Tre puntini** → **Ricarica**

### Nessun backup trovato

**Soluzione:**
1. Verifica che ci siano backup nel sistema: **Impostazioni** → **Sistema** → **Backup**
2. Controlla i log di Home Assistant per errori
3. L'integrazione richiede Home Assistant OS o Supervised (non funziona su Container o Core standalone)

## 📝 Log e Debug

Per abilitare i log dettagliati dell'integrazione, aggiungi al `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.backup_guardian: debug
```

Poi riavvia Home Assistant e controlla i log in **Impostazioni** → **Sistema** → **Log**.

## 🚀 Funzionalità Future

Pianificate per le prossime versioni:

- [ ] Supporto backup Google Drive
- [ ] Supporto backup Dropbox
- [ ] Supporto backup OneDrive
- [ ] Notifiche push personalizzate
- [ ] Grafici storici dei backup
- [ ] Backup differenziali
- [ ] Pulizia automatica backup vecchi
- [ ] Verifica integrità backup
- [ ] Export lista backup in CSV

## 🤝 Contribuire

Contributi, issue e richieste di funzionalità sono benvenuti!

### Come Contribuire

1. Fai un **Fork** del progetto
2. Crea un **branch** per la tua feature: `git checkout -b feature/AmazingFeature`
3. **Commit** delle modifiche: `git commit -m 'Add some AmazingFeature'`
4. **Push** sul branch: `git push origin feature/AmazingFeature`
5. Apri una **Pull Request**

### Segnalare Bug

Apri un [Issue](https://github.com/leonardus1973/backup-guardian/issues) con:
- Descrizione del problema
- Versione di Home Assistant
- Versione di Backup Guardian
- Log rilevanti

## 📄 Licenza

Questo progetto è distribuito con licenza **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Puoi usarlo, modificarlo e condividerlo liberamente, ma **non è consentito alcun utilizzo commerciale**. Per maggiori dettagli: https://creativecommons.org/licenses/by-nc/4.0/

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.
Commercial use is **explicitly forbidden** without prior written permission.
If you need a commercial license, please contact the author.

## 👤 Autore

**Leonardo** - [@leonardus1973](https://github.com/leonardus1973)

## 🙏 Ringraziamenti

- Community di Home Assistant
- HACS (Home Assistant Community Store)
- Tutti i contributori e tester

## ⭐ Supporto

Se questo progetto ti è utile, considera di:

- ⭐ Lasciare una **stella** su GitHub
- 🐛 Segnalare **bug** o suggerire **funzionalità**
- 📢 Condividere il progetto con altri utenti di Home Assistant

---

## 📋 Requisiti di Sistema

- **Home Assistant OS** 2023.1.0 o superiore
- **Home Assistant Supervised** 2023.1.0 o superiore

**Nota**: Questa integrazione **richiede** il Supervisor di Home Assistant per funzionare. Non è compatibile con:
- Home Assistant Container (Docker standalone)
- Home Assistant Core (installazione Python)

---

**Versione corrente**: 1.1.0  
**Ultimo aggiornamento**: Febbraio 2026

Per supporto, domande o feedback, apri un [Issue su GitHub](https://github.com/leonardus1973/backup-guardian/issues).

---

**Nota**: Questo è un progetto comunitario non ufficiale e non è affiliato con Home Assistant.
