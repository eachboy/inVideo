import { useEffect, useState } from 'react'

type Status = 'loading' | 'ok' | 'error'

function App() {
  const [status, setStatus] = useState<Status>('loading')

  useEffect(() => {
    fetch('/api/v1/health')
      .then((res) => (res.ok ? res.json() : Promise.reject(res.status)))
      .then((data: { status: string }) => {
        setStatus(data.status === 'ok' ? 'ok' : 'error')
      })
      .catch(() => setStatus('error'))
  }, [])

  const badge = {
    loading: 'bg-surface-muted text-text-muted',
    ok: 'bg-success text-white',
    error: 'bg-danger text-white',
  }[status]

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center gap-4 p-6">
      <h1 className="text-3xl font-bold text-accent">inVideo</h1>
      <p className="text-text-muted">Проверка соединения с API</p>
      <span className={`rounded-full px-4 py-1 text-sm font-medium ${badge}`}>
        {status === 'loading' ? 'проверяем…' : status === 'ok' ? 'API: ok' : 'API недоступен'}
      </span>
      <button className="rounded-lg bg-accent px-5 py-2 text-white hover:bg-accent-hover">
        Кнопка с акцентом
      </button>
      <button className="rounded-lg bg-warm px-5 py-2 text-white">Оранжевая</button>
    </main>
  )
}

export default App