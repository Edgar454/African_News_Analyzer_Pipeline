import ContactIcon from './ui/ContactIcon'

const IconGrid = () => (
  <div className="@container">
    <div className="gap-2 px-4 flex flex-wrap justify-start">
      <ContactIcon type="mail" />
      <ContactIcon type="github" />
      <ContactIcon type="linkedin" />
    </div>
  </div>
)

export default IconGrid
