import { Link } from 'react-router-dom';

const NavLinks = () => {
  return (
    <nav className="flex items-center gap-9">
      <Link className="text-sm font-medium leading-normal text-[#131416]" to="/news">News</Link>
      <Link className="text-sm font-medium leading-normal text-[#131416]" to="/summary">Summary</Link>
      <Link className="text-sm font-medium leading-normal text-[#131416]" to="/compare">Compare</Link>
      <Link className="text-sm font-medium leading-normal text-[#131416]" to="/about">About</Link>
    </nav>
  );
};

export default NavLinks;
