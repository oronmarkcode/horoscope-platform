type Props = {
    data: any
}

export default function HoroscopeCard({ data }: Props) {
    const d = data?.horoscope_data ? data.horoscope_data : data
    const payload = d?.payload_json || {}
    return (
        <div className="rounded-xl bg-gradient-to-b from-indigo-800 to-indigo-900 text-white p-5 shadow">
            <div className="text-sm opacity-80">{d?.zodiac_sign} · {d?.for_date}</div>
            {payload.headline && (
                <h3 className="text-2xl font-bold mt-1">{payload.headline}</h3>
            )}
            {(payload.reading || payload.content) && (
                <p className="mt-2 text-indigo-100 whitespace-pre-wrap">{payload.reading || payload.content}</p>
            )}
            <div className="mt-4 flex gap-4 text-sm">
                {payload.lucky_color && <span>Lucky color: <strong>{payload.lucky_color}</strong></span>}
                {payload.lucky_number && <span>Lucky number: <strong>{payload.lucky_number}</strong></span>}
                {payload.mood && <span>Mood: <strong>{payload.mood}</strong></span>}
            </div>
        </div>
    )
}


