// SearchBar.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && query.trim() !== '') {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
      setQuery('');
    }
  };

  return (
    <label className="flex flex-col min-w-40 !h-10 max-w-64">
      <div className="flex w-full items-stretch rounded-xl h-full">
        <div className="text-[#6b7580] flex border-none bg-[#f1f2f3] items-center justify-center pl-4 rounded-l-xl">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256">
            <path d="M229.66 218.34l-50.07-50.06a88.11 88.11 0 1 0-11.31 11.31l50.06 50.07a8 8 0 0 0 11.32-11.32ZM40 112a72 72 0 1 1 72 72 72.08 72.08 0 0 1-72-72Z"/>
          </svg>
        </div>
        <input
          className="form-input flex w-full flex-1 resize-none overflow-hidden rounded-xl text-[#131416] focus:outline-0 focus:ring-0 border-none bg-[#f1f2f3] px-4 rounded-l-none text-base"
          placeholder="Search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>
    </label>
  );
}
