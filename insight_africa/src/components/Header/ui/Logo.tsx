import { Link } from 'react-router-dom';

const Logo = () => {
  return (
    <Link to="/" className="flex items-center gap-4 text-[#131416] hover:opacity-80 transition-opacity">
      <div className="w-4 h-4">
        <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g clipPath="url(#clip0_6_330)">
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M24 0.757355L47.2426 24L24 47.2426L0.757355 24L24 0.757355ZM21 35.7574V12.2426L9.24264 24L21 35.7574Z"
              fill="currentColor"
            />
          </g>
          <defs>
            <clipPath id="clip0_6_330">
              <rect width="48" height="48" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </div>
      <h2 className="text-lg font-bold leading-tight tracking-[-0.015em]">Insight Africa</h2>
    </Link>
  );
};

export default Logo;
