import { useEffect, useState } from 'react'
import HoroscopeCard from '../components/HoroscopeCard'
import Modal from '../components/Modal'
import { useToast } from '../components/Toast'
import { api } from '../lib/api'
import { useAuth } from '../store/auth'

export default function Home() {
    const [name, setName] = useState('')
    const [dob, setDob] = useState('')
    const [timezone, setTimezone] = useState(Intl.DateTimeFormat().resolvedOptions().timeZone)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [result, setResult] = useState<any>(null)
    const [limitOpen, setLimitOpen] = useState(false)
    const toast = useToast()
    const { token } = useAuth()

    useEffect(() => {
        async function autoload() {
            if (!token) return
            try {
                setLoading(true)
                const today = new Date().toISOString().slice(0, 10)
                const listRes = await api.get('/api/v1/horoscopes', {
                    params: { from: today, to: today, limit: 1 },
                })
                if (Array.isArray(listRes.data) && listRes.data.length > 0) {
                    setResult(listRes.data[0])
                } else {
                    const createRes = await api.post('/api/v1/horoscopes', {})
                    setResult(createRes.data)
                }
            } catch {
                // ignore
            } finally {
                setLoading(false)
            }
        }
        autoload()
        // run once on mount when token present
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [token])

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const res = await api.post('/api/v1/horoscopes', {
                name,
                dob,
                timezone,
            })
            if (res.data?.status === 'insufficient_credits' || res.data?.status === 'limit_reached') {
                setLimitOpen(true)
            } else {
                setResult(res.data)
            }
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to generate')
            toast.push({ message: 'Failed to generate horoscope', type: 'error' })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-indigo-900 to-indigo-800 text-white">
            <div className="max-w-2xl mx-auto py-16 px-4">
                <h1 className="text-4xl font-bold mb-6">MyHoroscope</h1>
                <div className="bg-white/10 backdrop-blur rounded-xl p-6 shadow">
                    {!token ? (
                        <>
                            <h2 className="text-2xl font-semibold mb-4">Get your daily horoscope</h2>
                            <form onSubmit={onSubmit} className="space-y-4">
                                <input className="w-full px-3 py-2 rounded bg-white/20" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
                                <input className="w-full px-3 py-2 rounded bg-white/20" type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
                                <input className="w-full px-3 py-2 rounded bg-white/20" placeholder="Timezone" value={timezone} onChange={(e) => setTimezone(e.target.value)} />
                                <button disabled={loading} className="px-4 py-2 rounded bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50">{loading ? 'Generating...' : (result ? 'Regenerate' : 'Generate')}</button>
                            </form>
                            {error && <p className="text-red-300 mt-4">{error}</p>}
                            {result && (
                                <div className="mt-6">
                                    <HoroscopeCard data={result} />
                                </div>
                            )}
                        </>
                    ) : (
                        <>
                            <div className="flex items-center justify-between mb-3">
                                <h2 className="text-2xl font-semibold">Today’s Horoscope</h2>
                                <div className="flex gap-2">
                                    <button
                                        onClick={async () => {
                                            try {
                                                setLoading(true)
                                                const res = await api.post('/api/v1/horoscopes', {})
                                                setResult(res.data)
                                            } finally {
                                                setLoading(false)
                                            }
                                        }}
                                        className="px-3 py-1.5 rounded bg-indigo-600 hover:bg-indigo-500"
                                    >
                                        {loading ? 'Generating...' : 'Regenerate'}
                                    </button>
                                    <a href="/dashboard" className="px-3 py-1.5 rounded bg-white/10 hover:bg-white/20">History</a>
                                </div>
                            </div>
                            {loading && <div className="text-sm opacity-80">Generating…</div>}
                            {result && !loading && <HoroscopeCard data={result} />}
                        </>
                    )}
                </div>
            </div>
            <Modal
                open={limitOpen}
                onClose={() => setLimitOpen(false)}
                title="Daily limit reached"
                actions={<a href="/signup" className="px-3 py-1.5 rounded bg-indigo-600 text-white">Create account</a>}
            >
                <p>You’ve reached the anonymous usage limit. Create a free account to continue.</p>
            </Modal>
        </div>
    )
}


