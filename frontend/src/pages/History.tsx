import { useEffect, useState } from 'react'
import HoroscopeCard from '../components/HoroscopeCard'
import { api } from '../lib/api'

export default function History() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [rows, setRows] = useState<any[]>([])

    useEffect(() => {
        async function load() {
            setLoading(true)
            setError(null)
            try {
                const res = await api.get('/api/v1/horoscopes', { params: { limit: 20 } })
                setRows(res.data)
            } catch (err: any) {
                setError(err?.response?.data?.detail || 'Failed to load history')
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    return (
        <div className="min-h-screen bg-slate-900 text-white p-6">
            <h1 className="text-3xl font-bold mb-6">History</h1>
            {loading && <p>Loading...</p>}
            {error && <p className="text-red-300">{error}</p>}
            <div className="grid gap-4">
                {rows.map((r) => (
                    <div key={r.id} className="bg-white/10 rounded p-3">
                        <div className="text-sm opacity-80 mb-2">{r.for_date}{r.variation ? ` · var ${r.variation}` : ''}</div>
                        <HoroscopeCard data={r} />
                    </div>
                ))}
            </div>
        </div>
    )
}


