import { useState } from 'react';

export default function FilterButton({ label, options = [], onSelect, selected }) {
  const [open, setOpen] = useState(false);

  const displayLabel = selected || label;
  const isActive = Boolean(selected);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-xl px-4 pr-2 border transition-colors ${
          isActive
            ? 'bg-[#e0e7ff] text-[#1e40af] border-[#c7d2fe]'
            : 'bg-[#f1f2f3] text-[#131416] border-transparent'
        }`}
      >
        <p className="text-sm font-medium leading-normal">{displayLabel}</p>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          viewBox="0 0 256 256"
          className={`${isActive ? 'text-[#1e40af]' : 'text-[#131416]'}`}
        >
          <path d="M213.66 101.66l-80 80a8 8 0 0 1-11.32 0l-80-80A8 8 0 0 1 53.66 90.34L128 164.69l74.34-74.35a8 8 0 0 1 11.32 11.32Z" />
        </svg>
      </button>

      {open && (
        <div className="absolute z-10 mt-1 w-40 bg-white border border-gray-200 rounded shadow-md">
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => {
                onSelect(opt === 'All' ? null : opt);
                setOpen(false);
              }}
              className={`block w-full px-4 py-2 text-sm text-left hover:bg-gray-100 ${
                selected === opt ? 'bg-gray-100 font-semibold' : ''
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
