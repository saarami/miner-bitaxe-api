import React, { useEffect, useState } from 'react'
import StatusCards from './components/StatusCards'
import HistoryChart from './components/HistoryChart'
import CryptoPrices from './components/CryptoPrices'  

const POLL_INTERVAL_MS = 3000
const HISTORY_INTERVAL_MS = 10000
const CRYPTO_INTERVAL_MS = 30000  

export default function App() {
  const [status, setStatus] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState(null)
  const [crypto, setCrypto] = useState(null)  
  const [cryptoError, setCryptoError] = useState(null) // optional

  useEffect(() => {
    let statusTimer
    let historyTimer
    let cryptoTimer

    const fetchStatus = async () => {
      try {
        const res = await fetch('/api/miner/status')
        if (!res.ok) throw new Error('Failed to fetch status')
        const data = await res.json()
        setStatus(data)
        setError(null)
      } catch (err) {
        setError(err.message)
      }
    }

    const fetchHistory = async () => {
      try {
        const res = await fetch('/api/miner/history?limit=200')
        if (!res.ok) throw new Error('Failed to fetch history')
        const data = await res.json()
        setHistory(data)
      } catch (err) {
        // keep old history
      }
    }

    const fetchCrypto = async () => {        
      try {
        const res = await fetch('/api/crypto/prices')
        if (!res.ok) throw new Error('Failed to fetch crypto prices')
        const data = await res.json()
        setCrypto(data)
        setCryptoError(null)
      } catch (err) {
        setCryptoError(err.message)
      }
    }

    fetchStatus()
    fetchHistory()
    fetchCrypto()      // first call

    statusTimer = setInterval(fetchStatus, POLL_INTERVAL_MS)
    historyTimer = setInterval(fetchHistory, HISTORY_INTERVAL_MS)
    cryptoTimer = setInterval(fetchCrypto, CRYPTO_INTERVAL_MS)

    return () => {
      clearInterval(statusTimer)
      clearInterval(historyTimer)
      clearInterval(cryptoTimer)
    }
  }, [])

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Bitaxe Gamma 601 – Home Miner Dashboard</h1>
        <p className="subtitle">FastAPI + React + Vite</p>
      </header>

      {/* crypto prices below the header */}
      <CryptoPrices prices={crypto} />

      {error && <div className="error-banner">Error: {error}</div>}

      <main className="app-main">
        <StatusCards status={status} />
        <HistoryChart history={history} />
      </main>
    </div>
  )
}
