# 📥 Guida Completa all'Installazione - Backup Guardian

## Indice
1. [Prerequisiti](#prerequisiti)
2. [Metodo 1: Installazione via HACS (Consigliato)](#metodo-1-installazione-via-hacs)
3. [Metodo 2: Installazione Manuale](#metodo-2-installazione-manuale)
4. [Configurazione dell'Integrazione](#configurazione-dellintegrazione)
5. [Configurazione della Lovelace Card](#configurazione-della-lovelace-card)
6. [Verifica Installazione](#verifica-installazione)
7. [Risoluzione Problemi](#risoluzione-problemi)

---

## Prerequisiti

### Requisiti Minimi

- ✅ Home Assistant versione **2023.1.0** o superiore
- ✅ Accesso SSH o File Editor (per installazione manuale)
- ✅ HACS installato (per installazione via HACS)
- ✅ Backup presenti nella directory `/backup` di Home Assistant

### Verifica Versione Home Assistant

1. Vai su **Impostazioni** → **Info**
2. Controlla che la versione sia almeno **2023.1.0**

---

## Metodo 1: Installazione via HACS

### Passo 1: Aggiungi il Repository

1. Apri **HACS** nel menu laterale di Home Assistant
2. Clicca su **Integrazioni**
3. Clicca sui **tre puntini** in alto a destra
4. Seleziona **Repository personalizzati**
5. Nel campo **Repository** inserisci:
   ```
   https://github.com/leonardus1973/backup-guardian
   ```
6. Seleziona **Categoria**: `Integration`
7. Clicca su **Aggiungi**

### Passo 2: Installa l'Integrazione

1. In HACS → Integrazioni, cerca **"Backup Guardian"**
2. Clicca sull'integrazione
3. Clicca su **Scarica**
4. Seleziona l'ultima versione disponibile
5. Clicca su **Scarica** per confermare

### Passo 3: Riavvia Home Assistant

1. Vai su **Impostazioni** → **Sistema** → **Riavvia**
2. Conferma il riavvio
3. Attendi il completamento (circa 1-2 minuti)

---

## Metodo 2: Installazione Manuale

### Passo 1: Scarica i File

**Opzione A - Via Git:**
```bash
cd /config
git clone https://github.com/leonardus1973/backup-guardian.git
```

**Opzione B - Download Manuale:**
1. Vai su https://github.com/leonardus1973/backup-guardian
2. Clicca su **Code** → **Download ZIP**
3. Estrai il file ZIP

### Passo 2: Copia i File

1. Copia la cartella `custom_components/backup_guardian`
2. Incollala in `/config/custom_components/`
3. La struttura finale deve essere:
   ```
   /config/
   └── custom_components/
       └── backup_guardian/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── coordinator.py
           ├── sensor.py
           ├── manifest.json
           ├── strings.json
           ├── translations/
           │   └── it.json
           └── www/
               └── backup-guardian-card.js
   ```

### Passo 3: Verifica Permessi

Se usi Home Assistant OS o Supervised, i permessi sono gestiti automaticamente.

Per installazioni Core:
```bash
cd /config/custom_components
chown -R homeassistant:homeassistant backup_guardian
```

### Passo 4: Riavvia Home Assistant

```bash
# Via SSH
ha core restart

# Oppure dall'UI
# Impostazioni → Sistema → Riavvia
```

---

## Configurazione dell'Integrazione

### Passo 1: Aggiungi l'Integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Clicca sul pulsante **+ Aggiungi Integrazione** (in basso a destra)
3. Cerca **"Backup Guardian"**
4. Clicca sull'integrazione quando appare
5. Clicca su **Invia** per completare la configurazione

### Passo 2: Verifica i Sensori

1. Vai su **Strumenti per sviluppatori** → **Stati**
2. Cerca i sensori:
   - `sensor.ultimo_backup`
   - `sensor.totale_backup`
   - `sensor.dimensione_totale_backup`

Se vedi i sensori, l'integrazione è installata correttamente! ✅

---

## Configurazione della Lovelace Card

### Passo 1: Registra la Risorsa JavaScript

#### Metodo UI (Consigliato)

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Clicca su **+ Aggiungi risorsa**
3. Inserisci i seguenti dati:
   - **URL**: `/local/community/backup_guardian/backup-guardian-card.js`
   - **Tipo di risorsa**: **Modulo JavaScript**
4. Clicca su **Crea**

#### Metodo YAML

Aggiungi al file `configuration.yaml`:

```yaml
lovelace:
  mode: yaml
  resources:
    - url: /local/community/backup_guardian/backup-guardian-card.js
      type: module
```

Poi riavvia Home Assistant.

### Passo 2: Aggiungi la Card alla Dashboard

#### Metodo UI

1. Apri una dashboard
2. Clicca sui **tre puntini** in alto a destra → **Modifica dashboard**
3. Clicca su **+ Aggiungi Card**
4. Scorri in basso fino a trovare **Personalizzata: Backup Guardian Card**
5. Clicca sulla card
6. Nella configurazione, inserisci:
   ```yaml
   type: custom:backup-guardian-card
   entity: sensor.totale_backup
   last_backup_entity: sensor.ultimo_backup
   ```
7. Clicca su **Salva**

#### Metodo YAML

Aggiungi alla tua dashboard:

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

### Passo 3: Svuota la Cache del Browser

Importante per vedere le modifiche!

- **Chrome/Edge**: `Ctrl + Shift + R` (Windows) o `Cmd + Shift + R` (Mac)
- **Firefox**: `Ctrl + F5` (Windows) o `Cmd + Shift + R` (Mac)
- **Safari**: `Cmd + Option + R`

---

## Verifica Installazione

### Checklist Completa

- [ ] L'integrazione appare in **Dispositivi e Servizi**
- [ ] I 3 sensori sono visibili in **Strumenti per sviluppatori** → **Stati**
- [ ] La risorsa JavaScript è registrata in **Dashboard** → **Risorse**
- [ ] La card appare nella dashboard e mostra i dati
- [ ] Nessun errore nei log di Home Assistant

### Verifica Log

1. Vai su **Impostazioni** → **Sistema** → **Log**
2. Cerca eventuali errori relativi a `backup_guardian`
3. Se tutto OK, non dovrebbero esserci errori

---

## Risoluzione Problemi

### La card non appare nella lista

**Soluzione:**
1. Verifica che la risorsa JavaScript sia registrata
2. Svuota la cache del browser (Ctrl + F5)
3. Riavvia Home Assistant
4. Controlla che il file `backup-guardian-card.js` esista in:
   `/config/www/community/backup_guardian/`

### I sensori non vengono creati

**Soluzione:**
1. Verifica che l'integrazione sia aggiunta in **Dispositivi e Servizi**
2. Controlla i log per errori
3. Verifica che la directory `/backup` esista e contenga file `.tar`
4. Riavvia Home Assistant

### La card mostra "Nessun backup trovato"

**Soluzione:**
1. Verifica che ci siano backup in `/backup`
2. I backup devono avere estensione `.tar`
3. Controlla i permessi della directory `/backup`
4. Attendi 5 minuti (tempo di aggiornamento dei sensori)

### Errore "Entity not found"

**Soluzione:**
1. Verifica che i nomi dei sensori siano corretti:
   - `sensor.ultimo_backup`
   - `sensor.totale_backup`
2. Se hai rinominato i sensori, aggiorna la configurazione della card
3. Riavvia Home Assistant

### La card non si aggiorna

**Soluzione:**
1. I sensori si aggiornano ogni 5 minuti
2. Puoi forzare l'aggiornamento ricaricando la dashboard
3. Verifica la connessione con Home Assistant
4. Controlla che non ci siano errori nei log

### Problemi dopo l'aggiornamento

**Soluzione:**
1. Svuota completamente la cache del browser
2. Riavvia Home Assistant
3. Rimuovi e ri-aggiungi la risorsa JavaScript
4. Se il problema persiste, reinstalla l'integrazione

---

## Aggiornamento dell'Integrazione

### Via HACS

1. Apri HACS → Integrazioni
2. Cerca "Backup Guardian"
3. Se disponibile un aggiornamento, vedrai un pulsante **Aggiorna**
4. Clicca su **Aggiorna**
5. Riavvia Home Assistant

### Manuale

1. Scarica l'ultima versione da GitHub
2. Sostituisci la cartella `custom_components/backup_guardian`
3. Riavvia Home Assistant
4. Svuota la cache del browser

---

## Disinstallazione

### Rimuovi l'Integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Trova "Backup Guardian"
3. Clicca sui **tre puntini** → **Elimina**
4. Conferma l'eliminazione

### Rimuovi i File (Opzionale)

```bash
rm -rf /config/custom_components/backup_guardian
rm -rf /config/www/community/backup_guardian
```

### Rimuovi la Risorsa JavaScript

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Trova la risorsa `backup-guardian-card.js`
3. Clicca sull'icona del cestino per eliminarla

### Riavvia Home Assistant

---

## Supporto

Se hai ancora problemi:

1. 📝 Controlla i [Issues su GitHub](https://github.com/leonardus1973/backup-guardian/issues)
2. 🆕 Apri un nuovo Issue se il tuo problema non è già segnalato
3. 💬 Partecipa alle [Discussions](https://github.com/leonardus1973/backup-guardian/discussions)

---

**Buona installazione! 🚀**
