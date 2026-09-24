'use client'

import { FormEvent, useState } from 'react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function AICopilot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        'Hello! I am UrjaIQ Copilot. Ask me about energy consumption, machine anomalies, production performance, optimization, or carbon emissions.',
    },
  ])

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function sendMessage(event: FormEvent) {
    event.preventDefault()

    const message = input.trim()

    if (!message || loading) {
      return
    }

    setMessages((previous) => [
      ...previous,
      {
        role: 'user',
        content: message,
      },
    ])

    setInput('')
    setLoading(true)

    try {
      const API_BASE_URL =
        process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      const response = await fetch(`${API_BASE_URL}/api/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'AI request failed')
      }

      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          content: data.answer,
        },
      ])
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          content:
            error instanceof Error
              ? error.message
              : 'Unable to connect to UrjaIQ Copilot.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <section
      id="copilot"
      className="rounded-2xl border border-slate-800 bg-slate-900/40"
    >
      <div className="border-b border-slate-800 p-6">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-emerald-400">
              AI Copilot
            </p>

            <h2 className="mt-2 text-2xl font-semibold">Ask UrjaIQ</h2>

            <p className="mt-2 text-sm text-slate-400">
              Ask questions about your factory&apos;s energy, machines,
              production, optimization, and sustainability.
            </p>
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            AI Online
          </div>
        </div>
      </div>

      <div className="max-h-[420px] space-y-4 overflow-y-auto p-6">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                message.role === 'user'
                  ? 'bg-emerald-500 text-slate-950'
                  : 'border border-slate-800 bg-slate-950 text-slate-300'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-400">
              UrjaIQ is analyzing the latest factory data...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="border-t border-slate-800 p-4">
        <div className="flex gap-3">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about your factory..."
            disabled={loading}
            className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-emerald-500"
          />

          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? '...' : 'Send'}
          </button>
        </div>

        <p className="mt-2 px-1 text-xs text-slate-600">
          Press Enter to send • Responses are grounded in current UrjaIQ factory
          data.
        </p>
      </form>
    </section>
  )
}
