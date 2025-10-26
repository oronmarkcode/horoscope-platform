import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { useAuth } from '../store/auth'

export default function CreditsBadge() {
    const [text, setText] = useState<string>('')
    const { token } = useAuth()

    useEffect(() => {
        let mounted = true
        async function load() {
            try {
                const res = await api.get('/api/v1/usage')
                if (!mounted) return
                if (res.data.kind === 'regen_credits') {
                    setText(`${res.data.credits_remaining ?? 0} credits`)
                } else {
                    setText(`${res.data.attempts ?? 0} attempts today`)
                }
            } catch {
                // silent
            }
        }
        if (token) {
            load()
        }
        const id = token ? setInterval(load, 30000) : (null as any)
        return () => {
            mounted = false
            if (id) clearInterval(id)
        }
    }, [token])

    if (!token || !text) return null
    return (
        <span className="text-xs px-2 py-1 rounded-full bg-white/10">{text}</span>
    )
}


