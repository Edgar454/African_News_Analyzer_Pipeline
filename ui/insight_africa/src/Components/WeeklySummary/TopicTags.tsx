import React from 'react'
import {type  Topic } from '../../utils/api'

interface TopicModelTagsProps {
  topics: Topic[]
}

export default function TopicModelTags({ topics }: TopicModelTagsProps) {
  return (
    <div className="flex gap-3 p-3 flex-wrap pr-4">
      {topics.map((topic, i) => (
        <div
          key={i}
          className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-full bg-[#f1f2f3] pl-4 pr-4"
        >
          <p className="text-[#131416] text-sm font-medium leading-normal">
            Topic {i + 1}: {topic.terms.join(', ')}
          </p>
        </div>
      ))}
    </div>
  )
}
