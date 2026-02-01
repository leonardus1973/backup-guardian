# 🛡️ Backup Guardian - Custom Integration per Home Assistant

**Backup Guardian** è una custom integration per Home Assistant che monitora i backup locali, mostrando informazioni dettagliate come nome, data, ora, dimensione e hash SHA256 di verifica.

## ✨ Caratteristiche

- 📊 **Monitoraggio completo** dei backup locali di Home Assistant
- 🔍 **Verifica hash SHA256** per ogni backup
- 📈 **Sensori dedicati**:
  - Ultimo backup effettuato
  - Totale backup disponibili
  - Dimensione totale occupata
- 🎨 **Lovelace Card personalizzata** con interfaccia intuitiva
- 🔄 **Aggiornamento automatico** ogni 5 minuti
- 🚀 **Espandibile** per supportare Google Drive e altre piattaforme

## 📦 Installazione

### Metodo 1: HACS (Consigliato)

1. Apri **HACS** in Home Assistant
2. Vai su **Integrazioni**
3. Clicca sui tre puntini in alto a destra → **Repository personalizzati**
4. Aggiungi l'URL: `https://github.com/leonardus1973/backup-guardian`
5. Seleziona la categoria: **Integration**
6. Cerca "Backup Guardian" e installala
7. **Riavvia Home Assistant**

### Metodo 2: Installazione Manuale

1. Scarica la cartella `custom_components/backup_guardian`
2. Copiala nella directory `config/custom_components/` di Home Assistant
3. La struttura deve essere: `config/custom_components/backup_guardian/`
4. **Riavvia Home Assistant**

## ⚙️ Configurazione

### 1. Aggiungi l'integrazione

1. Vai su **Impostazioni** → **Dispositivi e Servizi**
2. Clicca su **+ Aggiungi Integrazione**
3. Cerca "Backup Guardian"
4. Clicca su **Invia** per completare la configurazione

### 2. Aggiungi la Lovelace Card

#### Metodo UI (Interfaccia grafica)

1. Vai in modalità modifica della dashboard
2. Clicca su **+ Aggiungi Card**
3. Scorri in basso e seleziona **Personalizzata: Backup Guardian Card**
4. Configura con:

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

#### Metodo YAML

Aggiungi alla tua dashboard Lovelace:

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

#### Card manuale

Aggiungi un nuova card ed incolla:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Backup Guardian - ultimo
    entities:
      - entity: sensor.backup_guardian_ultimo_backup
        name: Ultimo backup
        icon: mdi:calendar
      - type: attribute
        entity: sensor.backup_guardian_ultimo_backup
        attribute: backup_size
        name: Dimensione ultimo backup
        icon: mdi:floppy
      - type: attribute
        entity: sensor.backup_guardian_ultimo_backup
        name: Tipo backup
        attribute: backup_type
        icon: mdi:puzzle
      - type: attribute
        entity: sensor.backup_guardian_ultimo_backup
        attribute: backup_name
        name: Nome
        icon: mdi:folder
  - type: entities
    title: Backup Guardian - totali
    entities:
      - entity: sensor.backup_guardian_totale_backup
        name: Numero backup
      - entity: sensor.backup_guardian_dimensione_totale
        name: Dimensione totale
  - type: markdown
    title: Lista Backup
    content: >
      {% set backups = state_attr('sensor.backup_guardian_totale_backup',
      'backup_list') %}
      {% if backups %}
      **Backup trovati:**<br>
      {% for b in backups %}
          {% set ok = '✔️' if b.hash|length == 64 else '❌' %}
      🗂️ <b>{{ b.name }}</b><br>📅 {{ b.date }} &nbsp;&nbsp;⏰ {{ b.time }}<br>💾 {{ b.size }}<br>🔐 HASH: {{ ok }}<hr>
      {% endfor %}
      {% else %}
      _Nessun backup trovato._
      {% endif %}
```

### 3. Registra la risorsa JavaScript (necessario solo la prima volta)

1. Vai su **Impostazioni** → **Dashboard** → **Risorse**
2. Clicca su **+ Aggiungi risorsa**
3. Inserisci:
   - **URL**: `/local/community/backup_guardian/backup-guardian-card.js`
   - **Tipo di risorsa**: Modulo JavaScript
4. Clicca su **Crea**

**Oppure**, aggiungi manualmente al `configuration.yaml`:

```yaml
lovelace:
  resources:
    - url: /local/community/backup_guardian/backup-guardian-card.js
      type: module
```

## 📊 Sensori Disponibili

L'integrazione crea automaticamente 3 sensori:

### 1. `sensor.ultimo_backup`
Mostra la data e ora dell'ultimo backup effettuato.

**Attributi:**
- `backup_name`: Nome del file di backup
- `backup_date`: Data del backup
- `backup_time`: Ora del backup
- `backup_size`: Dimensione in MB
- `backup_hash`: Hash SHA256 per verifica integrità
- `backup_type`: Tipo di backup (local)

### 2. `sensor.totale_backup`
Indica il numero totale di backup presenti.

**Attributi:**
- `backup_list`: Lista completa di tutti i backup con i loro dettagli

### 3. `sensor.dimensione_totale_backup`
Mostra lo spazio totale occupato dai backup in MB.

## 🎨 Screenshot della Card

La card personalizzata mostra:

- **Sezione Ultimo Backup**: Informazioni dettagliate sull'ultimo backup
- **Bottone Totale Backup**: Mostra il numero totale e si espande per vedere la lista completa
- **Lista Espandibile**: Clic sul bottone per vedere tutti i backup con i loro dettagli

## 🔧 Configurazione Avanzata

### Modifica dell'intervallo di aggiornamento

Puoi modificare l'intervallo di aggiornamento (default: 5 minuti) editando il file `const.py`:

```python
UPDATE_INTERVAL = 300  # Secondi (300 = 5 minuti)
```

### Percorso personalizzato dei backup

Se i tuoi backup non sono in `/backup`, modifica il file `const.py`:

```python
BACKUP_PATH = "/percorso/personalizzato"
```

## 🚀 Funzionalità Future

- [ ] Supporto Google Drive
- [ ] Supporto Dropbox
- [ ] Notifiche su backup falliti
- [ ] Automazioni per pulizia backup vecchi
- [ ] Grafici storici
- [ ] Backup differenziali

## 🐛 Risoluzione Problemi

### I sensori non vengono creati

1. Verifica che l'integrazione sia installata correttamente
2. Controlla i log di Home Assistant: **Impostazioni** → **Sistema** → **Log**
3. Riavvia Home Assistant

### La card non appare

1. Verifica di aver registrato la risorsa JavaScript
2. Svuota la cache del browser (Ctrl + F5)
3. Controlla che l'URL della risorsa sia corretto

### Nessun backup trovato

1. Verifica che ci siano backup in `/backup`
2. Controlla i permessi della directory
3. Verifica che i backup abbiano estensione `.tar`

## 📝 Log e Debug

Per abilitare i log dettagliati, aggiungi al `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.backup_guardian: debug
```

## 🤝 Contribuire

Contributi, issue e richieste di funzionalità sono benvenuti!

1. Fai un Fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT.

## 👤 Autore

**Leonardo** - [@leonardus1973](https://github.com/leonardus1973)

## ⭐ Supporto

Se questo progetto ti è utile, considera di lasciare una stella su GitHub! ⭐

---

**Nota**: Questo è un progetto comunitario non ufficiale e non è affiliato con Home Assistant.
