import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import HoroscopeCard from '../components/HoroscopeCard'
import { api } from '../lib/api'

export default function Dashboard() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [today, setToday] = useState<any>(null)
    const [history] = useState<any[]>([])

    async function load() {
        setLoading(true)
        setError(null)
        try {
            const res = await api.post('/api/v1/horoscopes', {})
            setToday(res.data)
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to load')
        } finally {
            setLoading(false)
        }
    }

    async function regenerate() {
        try {
            await api.post('/api/v1/horoscopes', {})
            await load()
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to regenerate')
        }
    }

    async function generateCustom() {
        try {
            await api.post('/api/v1/horoscopes', { name: cName, dob: cDob, timezone: cTz })
            setCustomOpen(false)
            await load()
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to generate')
        }
    }

    useEffect(() => { load() }, [])

    return (
        <div className="min-h-screen bg-slate-900 text-white p-6">
            <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
            {loading && <p>Loading...</p>}
            {error && <p className="text-red-300">{error}</p>}
            {today && (
                <div className="mb-6">
                    <div className="flex items-center justify-between mb-3">
                        <h2 className="text-xl font-semibold">Today's Horoscope</h2>
                        <div className="flex gap-2">
                            <Link to="/history" className="px-3 py-1 rounded bg-white/10 hover:bg-white/20">History</Link>
                            <button onClick={regenerate} className="px-3 py-1 rounded bg-indigo-600 hover:bg-indigo-500">Regenerate</button>
                        </div>
                    </div>
                    <HoroscopeCard data={today} />
                    <p className="mt-2 text-sm opacity-80">Here’s something about your horoscope for today.</p>
                </div>
            )}
            {/* History moved to separate page */}
        </div>
    )
}


