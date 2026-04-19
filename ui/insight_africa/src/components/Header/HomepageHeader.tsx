import Logo from './ui/Logo';
import NavLinks from './ui/NavLinks';
import GetStartedButton from './ui/GetStartedButton';

const Header = () => {
  return (
    <header className="flex items-center justify-between whitespace-nowrap border-b border-[#f1f2f3] px-10 py-3">
      <Logo />
      <div className="flex flex-1 justify-end gap-8">
        <NavLinks />
        <GetStartedButton />
      </div>
    </header>
  );
};

export default Header;
