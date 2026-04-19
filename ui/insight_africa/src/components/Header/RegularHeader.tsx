import Logo from './ui/Logo';
import NavLinks from './ui/NavLinks';
import SearchBar from './ui/SearchBar';

const Header = () => {
  return (
    <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#f1f2f3] px-10 py-3">
      <div className="flex items-center gap-8">
        <Logo />
        <NavLinks />
      </div>
      <div className="flex flex-1 justify-end gap-8">
        <SearchBar />
      </div>
    </header>
  );
};

export default Header;
