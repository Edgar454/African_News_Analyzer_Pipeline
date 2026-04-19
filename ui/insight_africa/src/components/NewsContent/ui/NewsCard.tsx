import React from 'react'
import { useNavigate } from 'react-router-dom'
import { type NewsItem } from '../../../utils/api'

interface NewsCardProps {
  item: NewsItem
}

const NewsCard: React.FC<NewsCardProps> = ({ item }) => {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/news/${item.id}`)
  }

  return (
    <div
      onClick={handleClick}
      className="flex gap-4 bg-white px-4 py-3 justify-between transition duration-150 ease-in-out
                 hover:bg-gray-100 active:bg-gray-200 cursor-pointer rounded-lg"
    >
      <div className="flex items-start gap-4">
        <div
          className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg size-[70px]"
          style={{ backgroundImage: `url(https://source.unsplash.com/random/70x70?sig=${item.id})` }}
        ></div>
        <div className="flex flex-1 flex-col justify-center">
          <p className="text-[#131416] text-base font-medium leading-normal">{item.title}</p>
          <p className="text-[#6b7580] text-sm font-normal leading-normal">
            Published: {new Date(item.published_date).toLocaleDateString()} | Tags: {item.tags.join(', ')}
          </p>
          <div
            className="text-[#6b7580] text-sm font-normal leading-normal [&_a]:underline [&_strong]:font-semibold"
            dangerouslySetInnerHTML={{ __html: item.description }}
          ></div>
        </div>
      </div>
      <div className="shrink-0 flex items-center justify-center size-7 text-[#131416]">
        <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
          <path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z" />
        </svg>
      </div>
    </div>
  )
}

export default NewsCard
