import { useEffect, useState } from 'react'
import api from './lib/api'
import './App.css'

type AnyRec = Record<string, any>

export default function App() {
  const [items, setItems] = useState<AnyRec[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    setLoading(true)
    setError(null)
    api.get('/properties/')
      .then(res => {
        if (!alive) return
        const data = Array.isArray(res.data?.results) ? res.data.results : (Array.isArray(res.data) ? res.data : [])
        setItems(data)
      })
      .catch(err => {
        if (!alive) return
        setError(err?.message || 'Failed to load properties')
      })
      .finally(() => alive && setLoading(false))
    return () => { alive = false }
  }, [])

  return (
    <div className="min-h-screen p-6">
      <h1 className="mb-4 text-3xl font-bold text-indigo-700">Property237</h1>
      {loading && <p className="text-gray-600">Loading…</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && !error && (
        <ul className="space-y-2">
          {items.map((it, i) => (
            <li key={it.id ?? i} className="rounded border bg-white p-3 shadow-sm">
              <div className="font-semibold">{it.title || it.name || `Property ${it.id ?? i+1}`}</div>
              {it.slug && <div className="text-sm text-gray-500">{it.slug}</div>}
            </li>
          ))}
          {items.length === 0 && (
            <li className="text-gray-500">No properties found.</li>
          )}
        </ul>
      )}
    </div>
  )
}