# Backup Guardian v1.1.0

🛡️ **Prima versione stabile e completa!** Monitora i backup di Home Assistant con verifica hash SHA256 e badge destinazione.

## ✨ Novità v1.1.0

- ✅ **Copia automatica file card** - Zero configurazione manuale!
- ✅ **Badge destinazione** - Visualizza dove è salvato ogni backup
- ✅ **Orari corretti** - Fix timezone (non più -1h)
- ✅ **Struttura pronta** per Google Drive, Dropbox, OneDrive

## Caratteristiche

- 📊 Monitoraggio backup tramite Supervisor API
- 🔍 Hash SHA256 per ogni backup
- 📍 Badge destinazione colorati per ogni backup
- 📈 3 sensori: ultimo backup, totale, dimensione
- 🎨 Lovelace card moderna con design responsive
- 🔄 Aggiornamento automatico ogni 5 minuti
- ⏰ Timezone locale gestito correttamente
- 🌍 Interfaccia in italiano

## Installazione Rapida

### 1. Installa da HACS
Scarica "Backup Guardian" e **riavvia Home Assistant**.

✅ Il file JavaScript viene copiato automaticamente in `/config/www/community/backup_guardian/`!

### 2. Aggiungi Integrazione
**Impostazioni** → **Dispositivi e Servizi** → **+ Aggiungi Integrazione** → "Backup Guardian" → **Invia**

### 3. Registra Risorsa Card
**Impostazioni** → **Dashboard** → **Risorse** → **+ Aggiungi risorsa**

- URL: `/local/community/backup_guardian/backup-guardian-card.js`
- Tipo: **Modulo JavaScript**

⚠️ **IMPORTANTE**: Svuota cache browser dopo aver aggiunto la risorsa (Ctrl+Shift+R)!

### 4. Aggiungi Card
Dashboard → **Modifica** → **+ Aggiungi Card** → **Manuale**

```yaml
type: custom:backup-guardian-card
entity: sensor.backup_guardian_totale_backup
last_backup_entity: sensor.backup_guardian_ultimo_backup
size_entity: sensor.backup_guardian_dimensione_totale
```

## 🎨 Cosa Vedrai

- 📦 Ultimo backup con badge **[HOME ASSISTANT LOCALE]**
- 📊 Box statistiche: totale backup e MB occupati
- 🔘 Lista espandibile di tutti i backup
- 🏷️ Badge destinazione per ogni backup

## ⚠️ Importante

- **Richiede**: Home Assistant OS o Supervised
- **Dopo installazione**: Svuotare cache browser (Ctrl+Shift+R)
- **Se la card non appare**: Provare modalità incognito per verificare la cache

## 🐛 Risoluzione Problemi

### La card non si carica?
1. Verifica che il file esista: `/config/www/community/backup_guardian/backup-guardian-card.js`
2. Se manca, riavvia HA (viene copiato automaticamente)
3. Svuota cache browser completamente
4. Prova in modalità incognito

### Sensori vuoti?
1. Verifica di essere su HA OS o Supervised
2. Controlla log: Impostazioni → Sistema → Log
3. Cerca errori `backup_guardian`

### Badge destinazione non appaiono?
1. Verifica versione: deve essere **v1.1.0+**
2. Svuota cache completamente
3. Verifica attributo `backup_destination` nei sensori

## 📖 Documentazione

Documentazione completa, troubleshooting e esempi di automazioni nel [README](https://github.com/leonardus1973/backup-guardian).

## 🔜 Prossimi Sviluppi

- Google Drive integration
- Dropbox integration
- OneDrive integration
- Grafici storici
- Pulizia automatica backup vecchi

## 🐛 Segnala Bug

[Apri Issue](https://github.com/leonardus1973/backup-guardian/issues) per bug o richieste di funzionalità.

---

**Versione**: 1.1.0 - Prima Release Stabile  
**Requisiti**: Home Assistant 2023.1.0+  
**Licenza**: CC BY-NC 4.0  

Made with ❤️ in Italy 🇮🇹
