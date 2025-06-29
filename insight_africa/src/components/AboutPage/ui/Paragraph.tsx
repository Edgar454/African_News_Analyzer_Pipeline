interface ParagraphProps {
  children: React.ReactNode
}

const Paragraph: React.FC<ParagraphProps> = ({ children }) => (
  <p className="text-[#131416] text-base font-normal leading-normal pb-3 pt-1 px-4">
    {children}
  </p>
)

export default Paragraph
