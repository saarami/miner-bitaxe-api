
import React, { useMemo } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

export default function HistoryChart({ history }) {
  const data = useMemo(() => {
    if (!history || history.length === 0) return []
    return history
      .filter((h) => h.hash_rate != null)
      .map((h) => ({
        time: new Date(h.timestamp).toLocaleTimeString(),
        hash_rate: h.hash_rate,
      }))
  }, [history])

  return (
    <div className="card wide tall">
      <div className="card-header">
        <h2>Hashrate history</h2>
        <span className="chip chip-secondary">Last {data.length} points</span>
      </div>
      <div className="card-body chart-body">
        {data.length === 0 ? (
          <div>No history yet…</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <XAxis dataKey="time" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="hash_rate"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
