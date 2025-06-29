import  { useEffect, useRef } from 'react'

export default function TopicModelGraph() {
  const iframeRef = useRef<HTMLIFrameElement>(null)

  useEffect(() => {
    const fetchHTML = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/get_weekly_summary_visualization/topic_html`
        )
        const html = await res.text()

        if (iframeRef.current) {
          const iframeDoc = iframeRef.current.contentDocument || iframeRef.current.contentWindow?.document
          if (iframeDoc) {
            iframeDoc.open()
            iframeDoc.write(html)
            iframeDoc.close()
          }
        }
      } catch (err) {
        console.error('Failed to load pyLDAvis HTML:', err)
      }
    }

    fetchHTML()
  }, [])

  return (
    <div className="w-full px-4 py-3">
      <iframe
        ref={iframeRef}
        title="Topic Model Visualization"
        className="w-full h-[700px] border-none"
      />
    </div>
  )
}
