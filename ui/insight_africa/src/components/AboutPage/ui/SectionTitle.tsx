interface SectionTitleProps {
  children: React.ReactNode
}

const SectionTitle: React.FC<SectionTitleProps> = ({ children }) => (
  <h3 className="text-[#131416] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
    {children}
  </h3>
)

export default SectionTitle
