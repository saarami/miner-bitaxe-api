
import React from 'react'

export default function StatusCards({ status }) {
  if (!status) {
    return <div className="cards-grid">Loading miner status…</div>
  }


  function formatDifficulty(value) {
    if (value == null) return "—";
  
    const units = ["", "K", "M", "G", "T", "P", "E"];
    let unitIndex = 0;
  
    while (value >= 1000 && unitIndex < units.length - 1) {
      value /= 1000;
      unitIndex++;
    }
  
    return value.toFixed(2) + " " + units[unitIndex];
  }
  
  const onlineText = status.online ? 'ONLINE' : 'OFFLINE'
  const onlineClass = status.online ? 'chip chip-online' : 'chip chip-offline'

  const ts = new Date(status.timestamp)

  return (
    <div className="cards-grid">
      <div className="card wide">
        <div className="card-header">
          <h2>Miner Status</h2>
          <span className={onlineClass}>{onlineText}</span>
        </div>
        <div className="card-body row">
          <div>
            <div className="label">Last update</div>
            <div className="value">
              {ts.toLocaleDateString()} {ts.toLocaleTimeString()}
            </div>
          </div>
          <div>
            <div className="label">Hashrate</div>
            <div className="value">
              {status.hash_rate != null ? `${status.hash_rate.toFixed(2)} GH/s` : '—'}
            </div>
          </div>
          <div>
            <div className="label">Best Difficulty</div>
            <div className="value">
              {formatDifficulty(status.best_difficulty)}
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Temperatures</h3>
        </div>
        <div className="card-body">
          <div className="label">Core</div>
          <div className="value">
            {status.temp_core != null ? `${status.temp_core.toFixed(1)} °C` : '—'}
          </div>
          <div className="label mt">VRM</div>
          <div className="value">
            {status.temp_vr != null ? `${status.temp_vr.toFixed(1)} °C` : '—'}
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Frequency & Voltage</h3>
        </div>
        <div className="card-body">
          <div className="label">Frequency</div>
          <div className="value">
            {status.frequency != null ? `${status.frequency} MHz` : '—'}
          </div>
          <div className="label mt">Core Voltage</div>
          <div className="value">
            {status.core_voltage != null ? `${status.core_voltage.toFixed(0)} mV` : '—'}
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Shares</h3>
        </div>
        <div className="card-body">
          <div className="label">Accepted</div>
          <div className="value">
            {status.shares_accepted != null ? status.shares_accepted : '—'}
          </div>
          <div className="label mt">Rejected</div>
          <div className="value">
            {status.shares_rejected != null ? status.shares_rejected : '—'}
          </div>
        </div>
      </div>
    </div>
  )
}
