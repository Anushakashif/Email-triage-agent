'use client'

import { useEffect, useState } from "react"
import axios from "axios"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"

interface Draft {
  id: string
  from: string
  subject: string
  snippet: string
  urgency: string
  category: string
  draft: string
}

export default function ReviewPage() {
  const [drafts, setDrafts] = useState<Draft[]>([])
  const [approved, setApproved] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [sent, setSent] = useState(false)

  useEffect(() => {
    fetchDrafts()
  }, [])

  const fetchDrafts = async () => {
    try {
      const res = await axios.get(`${API_URL}/drafts`)
      setDrafts(res.data.drafts)
    } catch (err) {
      console.error("Failed to fetch drafts", err)
    } finally {
      setLoading(false)
    }
  }

  const toggleApprove = (id: string) => {
    setApproved(prev =>
      prev.includes(id) ? prev.filter(a => a !== id) : [...prev, id]
    )
  }

  const sendApproved = async () => {
    setSending(true)
    try {
      await axios.post(`${API_URL}/approve`, approved)
      setSent(true)
    } catch (err) {
      console.error("Failed to send", err)
    } finally {
      setSending(false)
    }
  }

  const urgencyColor = (urgency: string) => {
    if (urgency === "urgent") return "text-red-500"
    if (urgency === "normal") return "text-yellow-500"
    return "text-green-500"
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-900">
      Loading drafts...
    </div>
  )

  if (sent) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-900">
      <div className="text-center">
        <div className="text-5xl mb-4">✅</div>
        <h1 className="text-2xl font-bold">Emails Sent Successfully</h1>
        <p className="text-gray-500 mt-2">Your approved replies have been sent.</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8">
      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📧 Email Review</h1>
          <p className="text-gray-500 mt-1">
            Select drafts to approve and send
          </p>
        </div>

        {/* No drafts */}
        {drafts.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            No drafts available. Run the agent first.
          </div>
        )}

        {/* Draft cards */}
        {drafts.map(draft => (
          <div
            key={draft.id}
            className={`mb-4 p-5 rounded-xl border transition-all cursor-pointer ${
              approved.includes(draft.id)
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200 bg-white"
            }`}
            onClick={() => toggleApprove(draft.id)}
          >
            {/* Email info */}
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="font-semibold text-lg text-gray-900">{draft.subject}</p>
                <p className="text-gray-500 text-sm">{draft.from}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-sm font-medium ${urgencyColor(draft.urgency)}`}>
                  {draft.urgency}
                </span>
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                  approved.includes(draft.id)
                    ? "border-blue-500 bg-blue-500"
                    : "border-gray-300"
                }`}>
                  {approved.includes(draft.id) && <span className="text-xs text-white">✓</span>}
                </div>
              </div>
            </div>

            {/* Snippet */}
            <p className="text-gray-500 text-sm mb-3">{draft.snippet}</p>

            {/* Draft reply */}
            <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
              <p className="text-xs text-gray-400 mb-1">Draft Reply:</p>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{draft.draft}</p>
            </div>
          </div>
        ))}

        {/* Send button */}
        {drafts.length > 0 && (
          <div className="mt-6 flex justify-between items-center">
            <p className="text-gray-500">
              {approved.length} of {drafts.length} selected
            </p>
            <button
              onClick={sendApproved}
              disabled={approved.length === 0 || sending}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all"
            >
              {sending ? "Sending..." : `Send ${approved.length} Replies`}
            </button>
          </div>
        )}

      </div>
    </div>
  )
}