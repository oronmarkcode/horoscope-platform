import { useEffect, useState } from 'react'
import Modal from '../components/Modal'
import { api } from '../lib/api'

export default function Profile() {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [name, setName] = useState('')
    const [dob, setDob] = useState('')
    const [timezone, setTimezone] = useState('')
    const [dailyEmailEnabled, setDailyEmailEnabled] = useState(false)
    const [comingSoonOpen, setComingSoonOpen] = useState(false)

    async function load() {
        setLoading(true)
        setError(null)
        try {
            const res = await api.get('/api/v1/profile')
            setName(res.data.name)
            setDob(res.data.dob)
            setTimezone(res.data.timezone)
            setDailyEmailEnabled(res.data.daily_email_enabled)
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to load profile')
        } finally {
            setLoading(false)
        }
    }

    async function save() {
        try {
            await api.put('/api/v1/profile', { name, dob, timezone, daily_email_enabled: dailyEmailEnabled })
            if (dailyEmailEnabled) setComingSoonOpen(true)
            await load()
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Failed to save profile')
        }
    }

    useEffect(() => { load() }, [])

    return (
        <div className="min-h-screen bg-slate-900 text-white p-6">
            <h1 className="text-3xl font-bold mb-6">Profile</h1>
            {loading && <p>Loading...</p>}
            {error && <p className="text-red-300">{error}</p>}
            <div className="grid gap-3 max-w-lg">
                <input className="px-3 py-2 rounded bg-white/10" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                <input className="px-3 py-2 rounded bg-white/10" type="date" value={dob} onChange={(e) => setDob(e.target.value)} />
                <input className="px-3 py-2 rounded bg-white/10" placeholder="Timezone" value={timezone} onChange={(e) => setTimezone(e.target.value)} />
                <label className="inline-flex items-center gap-2"><input type="checkbox" checked={dailyEmailEnabled} onChange={(e) => setDailyEmailEnabled(e.target.checked)} /><span>Email notifications</span></label>
                <div>
                    <button onClick={save} className="px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-500">Save</button>
                </div>
            </div>
            <Modal
                open={comingSoonOpen}
                onClose={() => setComingSoonOpen(false)}
                title="Coming soon!"
            >
                <p>Email notifications will be available shortly.</p>
            </Modal>
        </div>
    )
}


