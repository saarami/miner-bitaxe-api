import React from 'react'

export default function CryptoPrices({ prices }) {
  if (!prices) {
    return (
      <div className="crypto-bar">
        <span className="label">Crypto prices</span>
        <span className="value">Loading…</span>
      </div>
    )
  }

  const time = new Date(prices.last_updated)

  return (
    <div className="crypto-bar">
      <span className="label">Crypto prices</span>
      <span className="value">
        BTC: ${prices.btc_usd.toLocaleString(undefined, { maximumFractionDigits: 2 })} &nbsp;|&nbsp;
        ETH: ${prices.eth_usd.toLocaleString(undefined, { maximumFractionDigits: 2 })}
      </span>
      <span className="label small">
        Updated: {time.toLocaleTimeString()}
      </span>
    </div>
  )
}
