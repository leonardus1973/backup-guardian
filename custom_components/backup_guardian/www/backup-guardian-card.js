class BackupGuardianCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._expanded = false;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Devi definire un entity (sensor.backup_guardian_totale_backup)');
    }
    this.config = config;
  }

  set hass(hass) {
    const oldHass = this._hass;
    this._hass = hass;
    
    if (!this.content) {
      this._createCard();
      this._updateCard();
      return;
    }
    
    // Se la lista è espansa, NON aggiornare (per evitare scroll reset)
    if (this._expanded) {
      return;
    }
    
    // Aggiorna SOLO se i dati sono cambiati
    const entityId = this.config.entity;
    const oldEntity = oldHass?.states[entityId];
    const newEntity = hass.states[entityId];
    
    if (!oldEntity || 
        oldEntity.state !== newEntity.state ||
        JSON.stringify(oldEntity.attributes.backup_list) !== JSON.stringify(newEntity.attributes.backup_list)) {
      this._updateCard();
    }
  }

  _getDestinationColor(destination) {
    // Mappa colori UFFICIALI dei brand
    // Supporta sia codici (local, google_drive) che nomi friendly
    const colors = {
      // Codici
      'local': '#03A9F4',
      'google_drive': '#4CAF50',
      'dropbox': '#0061FF',
      'onedrive': '#E74C3C',
      'nas': '#FF9800',
      'ftp': '#9C27B0',
      // Nomi friendly (case-insensitive)
      'home assistant locale': '#03A9F4',
      'google drive': '#4CAF50',
      'dropbox': '#0061FF',
      'onedrive': '#E74C3C',
      'nas': '#FF9800',
      'ftp': '#9C27B0',
    };
    
    // Cerca sia minuscolo che esatto
    const key = destination.toLowerCase();
    return colors[key] || colors[destination] || '#03A9F4';
  }

  _getDestinationName(destination) {
    // Nomi friendly per destinazioni
    const names = {
      'local': 'HOME ASSISTANT LOCALE',
      'google_drive': 'GOOGLE DRIVE',
      'dropbox': 'DROPBOX',
      'onedrive': 'ONEDRIVE',
      'nas': 'NAS',
      'ftp': 'FTP',
    };
    return names[destination] || destination.toUpperCase();
  }

  _createCard() {
    const style = document.createElement('style');
    style.textContent = `
      .backup-card {
        padding: 16px;
        background: var(--ha-card-background, var(--card-background-color, white));
        border-radius: var(--ha-card-border-radius, 12px);
        box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1));
      }
      
      .header {
        display: flex;
        align-items: center;
        margin-bottom: 16px;
        font-size: 18px;
        font-weight: 500;
        color: var(--primary-text-color);
      }
      
      .header-icon {
        margin-right: 12px;
        font-size: 24px;
      }
      
      .last-backup {
        background: var(--primary-background-color);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
      }
      
      .backup-info {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 8px;
        font-size: 14px;
      }
      
      .label {
        font-weight: 500;
        color: var(--secondary-text-color);
      }
      
      .value {
        color: var(--primary-text-color);
      }

      .destination-badge {
        display: inline-block;
        padding: 2px 8px;
        color: white;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
      }
      
      .hash {
        font-family: monospace;
        font-size: 12px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      
      .total-button {
        width: 100%;
        padding: 12px;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.3s ease;
      }
      
      .total-button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
      }

      .chevron {
        display: inline-block;
        transition: transform 0.3s ease;
        font-size: 20px;
      }
      
      .total-button.expanded .chevron {
        transform: rotate(180deg);
      }
      
      .backup-list {
        margin-top: 12px;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
      }
      
      .backup-list.expanded {
        max-height: 500px;
        overflow-y: auto;
      }
      
      .backup-item {
        background: var(--primary-background-color);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid;
      }

      .backup-item-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      }
      
      .no-backups {
        text-align: center;
        padding: 24px;
        color: var(--secondary-text-color);
      }
      
      .section-title {
        font-size: 14px;
        font-weight: 500;
        color: var(--secondary-text-color);
        margin-bottom: 8px;
      }

      .stats-row {
        display: flex;
        gap: 12px;
        margin-top: 12px;
      }

      .stat-box {
        flex: 1;
        background: var(--primary-background-color);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
      }

      .stat-value {
        font-size: 20px;
        font-weight: 600;
        color: var(--primary-color);
      }

      .stat-label {
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 4px;
      }
    `;
    
    this.content = document.createElement('div');
    this.content.className = 'backup-card';
    
    this.shadowRoot.appendChild(style);
    this.shadowRoot.appendChild(this.content);
  }

  _updateCard() {
    const entityId = this.config.entity;
    const lastBackupEntity = this.config.last_backup_entity || 'sensor.backup_guardian_ultimo_backup';
    const sizeEntity = this.config.size_entity || 'sensor.backup_guardian_dimensione_totale';
    
    const totalEntity = this._hass.states[entityId];
    const lastEntity = this._hass.states[lastBackupEntity];
    const sizeEntityObj = this._hass.states[sizeEntity];
    
    if (!totalEntity) {
      this.content.innerHTML = '<div class="no-backups">Entità non trovata: ' + entityId + '</div>';
      return;
    }
    
    const totalBackups = totalEntity.state;
    const backupList = totalEntity.attributes.backup_list || [];
    const totalSize = sizeEntityObj ? sizeEntityObj.state : '0';
    
    let lastBackupHtml = '';
    if (lastEntity && lastEntity.state !== 'Nessun backup') {
      const attrs = lastEntity.attributes;
      const destination = attrs.backup_destination || 'Home Assistant Locale';
      const destinationColor = this._getDestinationColor(destination);
      
      lastBackupHtml = `
        <div class="section-title">📦 Ultimo Backup</div>
        <div class="last-backup">
          <div class="backup-info">
            <span class="label">Nome:</span>
            <span class="value">${attrs.backup_name || 'N/A'}</span>
            
            <span class="label">Destinazione:</span>
            <span class="value">
              <span class="destination-badge" style="background: ${destinationColor};">
                ${destination}
              </span>
            </span>
            
            <span class="label">Data:</span>
            <span class="value">${attrs.backup_date || 'N/A'}</span>
            
            <span class="label">Ora:</span>
            <span class="value">${attrs.backup_time || 'N/A'}</span>
            
            <span class="label">Dimensione:</span>
            <span class="value">${attrs.backup_size || 'N/A'}</span>
            
            <span class="label">Hash:</span>
            <span class="value hash" title="${attrs.backup_hash || 'N/A'}">
              ${attrs.backup_hash ? attrs.backup_hash.substring(0, 16) + '...' : 'N/A'}
            </span>
          </div>
        </div>
      `;
    }
    
    this.content.innerHTML = `
      <div class="header">
        <span class="header-icon">🛡️</span>
        Backup Guardian
      </div>
      
      ${lastBackupHtml}

      <div class="stats-row">
        <div class="stat-box">
          <div class="stat-value">${totalBackups}</div>
          <div class="stat-label">Backup Totali</div>
        </div>
        <div class="stat-box">
          <div class="stat-value">${totalSize}</div>
          <div class="stat-label">MB Totali</div>
        </div>
      </div>
      
      <button class="total-button ${this._expanded ? 'expanded' : ''}" id="toggleBtn">
        <span>Mostra Tutti i Backup</span>
        <span class="chevron">▼</span>
      </button>
      
      <div class="backup-list ${this._expanded ? 'expanded' : ''}" id="backupList">
        ${backupList.length > 0 ? backupList.map((backup, index) => {
          // Destination è già il nome friendly
          const destination = backup.destination || 'Home Assistant Locale';
          const destinationColor = this._getDestinationColor(destination);
          
          return `
          <div class="backup-item" style="border-left-color: ${destinationColor};">
            <div class="backup-item-header">
              <strong>${backup.name}</strong>
              <span class="destination-badge" style="background: ${destinationColor};">
                ${destination}
              </span>
            </div>
            <div class="backup-info">
              <span class="label">Data/Ora:</span>
              <span class="value">${backup.date} ${backup.time}</span>
              
              <span class="label">Dimensione:</span>
              <span class="value">${backup.size}</span>
              
              <span class="label">Hash:</span>
              <span class="value hash" title="${backup.hash}">
                ${backup.hash.substring(0, 16)}...
              </span>
            </div>
          </div>
        `;
        }).join('') : '<div class="no-backups">Nessun backup trovato</div>'}
      </div>
    `;
    
    // Aggiungi event listener al bottone toggle
    const toggleBtn = this.shadowRoot.getElementById('toggleBtn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        this._expanded = !this._expanded;
        this._updateCard();
      });
    }
  }

  getCardSize() {
    return 3;
  }
}

// Definisci il custom element
customElements.define('backup-guardian-card', BackupGuardianCard);

// Registra la card in Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'backup-guardian-card',
  name: 'Backup Guardian Card',
  description: 'Card personalizzata per visualizzare i backup di Home Assistant',
  preview: true,
});

console.log('✅ Backup Guardian Card loaded successfully!');