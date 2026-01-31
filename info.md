# Backup Guardian

Monitora i backup di Home Assistant con verifica hash SHA256.

## Caratteristiche

- 📊 Monitoraggio backup locali
- 🔍 Verifica integrità con hash SHA256
- 📈 Sensori per ultimo backup, totale e dimensione
- 🎨 Lovelace card personalizzata
- 🔄 Aggiornamento automatico ogni 5 minuti

## Installazione

Dopo l'installazione via HACS:

1. **Riavvia Home Assistant**
2. Vai su Impostazioni → Dispositivi e Servizi
3. Aggiungi "Backup Guardian"
4. Registra la risorsa JavaScript:
   - Impostazioni → Dashboard → Risorse
   - URL: `/local/community/backup_guardian/backup-guardian-card.js`
   - Tipo: Modulo JavaScript

## Configurazione Card

```yaml
type: custom:backup-guardian-card
entity: sensor.totale_backup
last_backup_entity: sensor.ultimo_backup
```

Per maggiori dettagli, consulta il [README completo](https://github.com/leonardus1973/backup-guardian).
