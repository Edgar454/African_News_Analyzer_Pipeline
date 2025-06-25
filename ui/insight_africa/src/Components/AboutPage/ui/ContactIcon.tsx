interface ContactIconProps {
  type: 'mail' | 'github' | 'linkedin'
}

const icons = {
  mail: {
    label: 'Mail',
    link: 'mailto:meaved4@gmail.com',
    svg: (
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256">
        <path d="M224,48H32a8,8,0,0,0-8,8V192a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A8,8,0,0,0,224,48Zm-96,85.15L52.57,64H203.43ZM98.71,128,40,181.81V74.19Zm11.84,10.85,12,11.05a8,8,0,0,0,10.82,0l12-11.05,58,53.15H52.57ZM157.29,128,216,74.18V181.82Z" />
      </svg>
    ),
  },
  github: {
    label: 'GitHub',
    link: 'https://github.com/Edgar454/', // Update with your actual GitHub
    svg: (
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256">
        <path d="M208.31,75.68A59.78,59.78,0,0,0,202.93,28,8,8,0,0,0,196,24a59.75,59.75,0,0,0-48,24H124A59.75,59.75,0,0,0,76,24a8,8,0,0,0-6.93,4,59.78,59.78,0,0,0-5.38,47.68A58.14,58.14,0,0,0,56,104v8a56.06,56.06,0,0,0,48.44,55.47A39.8,39.8,0,0,0,96,192v8H72a24,24,0,0,1-24-24A40,40,0,0,0,8,136a8,8,0,0,0,0,16,24,24,0,0,1,24,24,40,40,0,0,0,40,40H96v16a8,8,0,0,0,16,0V192a24,24,0,0,1,48,0v40a8,8,0,0,0,16,0V192a39.8,39.8,0,0,0-8.44-24.53A56.06,56.06,0,0,0,216,112v-8A58.14,58.14,0,0,0,208.31,75.68Z" />
      </svg>
    ),
  },
  linkedin: {
    label: 'LinkedIn',
    link: 'https://linkedin.com/company/insightafrica', // Update with your actual LinkedIn
    svg: (
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256">
        <path d="M216,24H40A16,16,0,0,0,24,40V216a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V40A16,16,0,0,0,216,24Zm-120,88v64a8,8,0,0,1-16,0V112a8,8,0,0,1,16,0Zm88,28v36a8,8,0,0,1-16,0V140a20,20,0,0,0-40,0v36a8,8,0,0,1-16,0V112a8,8,0,0,1,15.79-1.78A36,36,0,0,1,184,140Zm-84-44a12,12,0,1,1-12-12A12,12,0,0,1,100,96Z" />
      </svg>
    ),
  },
}

const ContactIcon: React.FC<ContactIconProps> = ({ type }) => {
  const { svg, label, link } = icons[type]

  return (
    <a
      href={link}
      target="_blank"
      rel="noopener noreferrer"
      className="flex flex-col items-center gap-2 bg-white py-2.5 text-center w-20 
                 rounded-md transition-transform duration-200 hover:scale-105 hover:bg-gray-100"
    >
      <div className="rounded-full bg-[#f1f2f3] p-2.5 text-[#131416]">{svg}</div>
      <p className="text-[#131416] text-sm font-medium leading-normal">{label}</p>
    </a>
  )
}

export default ContactIcon
