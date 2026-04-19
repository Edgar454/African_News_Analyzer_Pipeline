// components/Pagination.tsx
import React from 'react'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1)

  return (
    <div className="flex items-center justify-center p-4 gap-1">
      <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1}>
        ←
      </button>
      {pages.map((page) => (
        <button
          key={page}
          className={`size-10 rounded-full flex items-center justify-center text-sm ${
            page === currentPage ? 'bg-[#f1f2f3] font-bold' : ''
          }`}
          onClick={() => onPageChange(page)}
        >
          {page}
        </button>
      ))}
      <button onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === totalPages}>
        →
      </button>
    </div>
  )
}

export default Pagination
