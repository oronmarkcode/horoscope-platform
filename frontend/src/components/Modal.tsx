import { ReactNode } from 'react'

type Props = {
    open: boolean
    title?: string
    onClose: () => void
    children: ReactNode
    actions?: ReactNode
}

export default function Modal({ open, title, onClose, children, actions }: Props) {
    if (!open) return null
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/60" onClick={onClose} />
            <div className="relative bg-white rounded-lg shadow-xl max-w-lg w-full mx-4">
                {title && (
                    <div className="px-5 py-3 border-b">
                        <h3 className="text-lg font-semibold">{title}</h3>
                    </div>
                )}
                <div className="p-5 text-slate-700">{children}</div>
                <div className="px-5 py-3 border-t flex justify-end gap-2 bg-slate-50">
                    {actions}
                    <button onClick={onClose} className="px-3 py-1.5 rounded bg-slate-200 hover:bg-slate-300">Close</button>
                </div>
            </div>
        </div>
    )
}


