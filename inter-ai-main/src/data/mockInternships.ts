export interface Internship {
  id: string;
  role: string;
  companyName: string;
  location: string;
  duration: number; // in months
  stipend: number; // monthly amount
  internType: string[];
  skills: string[];
  perks: string[];
  hiringSince: string;
  openings: number;
  applicants: number;
  websiteLink?: string;
  education?: string;
}

export const mockInternships: Internship[] = [
  {
    id: "2456465",
    role: "Machine Learning Internship",
    companyName: "Avaari",
    location: "Delhi, Bangalore, Mumbai, Chennai, Hyderabad",
    duration: 2,
    stipend: 25000,
    internType: ["Part time"],
    skills: ["Python", "Machine Learning", "Deep Learning", "Data Science", "Natural Language Processing"],
    perks: ["Certificate", "Letter of recommendation", "Flexible work hours"],
    hiringSince: "March 2023",
    openings: 2,
    applicants: 156,
    websiteLink: "https://avaari.com",
    education: "Graduation"
  },
  {
    id: "2456478",
    role: "Full Stack Development Internship",
    companyName: "Techvolt Software",
    location: "Chennai, Coimbatore, Bangalore, Delhi, Mumbai",
    duration: 3,
    stipend: 15000,
    internType: ["Full time"],
    skills: ["React", "Node.js", "JavaScript", "TypeScript", "MongoDB", "Express.js"],
    perks: ["Certificate", "Job offer", "5 days a week", "Informal dress code"],
    hiringSince: "January 2023",
    openings: 3,
    applicants: 234,
    websiteLink: "https://techvolt.com",
    education: "Graduation"
  },
  {
    id: "2452185",
    role: "Data Analytics Internship",
    companyName: "DataInsights Pro",
    location: "Delhi, Gurgaon, Noida, Bangalore",
    duration: 4,
    stipend: 20000,
    internType: ["Full time", "Work from home"],
    skills: ["Python", "SQL", "Tableau", "Power BI", "Data Analysis", "Statistics"],
    perks: ["Certificate", "Letter of recommendation", "Work from home", "Performance bonus"],
    hiringSince: "April 2023",
    openings: 2,
    applicants: 189,
    websiteLink: "https://datainsights.pro",
    education: "Graduation"
  },
  {
    id: "2450936",
    role: "Digital Marketing Internship",
    companyName: "Growth Hackers Agency",
    location: "Mumbai, Pune, Delhi, Bangalore",
    duration: 3,
    stipend: 12000,
    internType: ["Full time"],
    skills: ["SEO", "Social Media Marketing", "Content Writing", "Google Analytics", "Email Marketing"],
    perks: ["Certificate", "Letter of recommendation", "Free snacks & beverages"],
    hiringSince: "September 2022",
    openings: 4,
    applicants: 145,
    websiteLink: "https://growthhackers.agency",
    education: "Graduation"
  },
  {
    id: "2450882",
    role: "UI/UX Design Internship",
    companyName: "Creative Studios",
    location: "Bangalore, Mumbai, Delhi, Hyderabad",
    duration: 3,
    stipend: 18000,
    internType: ["Full time", "Remote"],
    skills: ["Figma", "Adobe XD", "Sketch", "User Research", "Prototyping", "Design Thinking"],
    perks: ["Certificate", "Letter of recommendation", "Flexible work hours", "Remote work"],
    hiringSince: "October 2022",
    openings: 2,
    applicants: 167,
    websiteLink: "https://creativestudios.design",
    education: "Graduation"
  },
  {
    id: "2461135",
    role: "Business Development Internship",
    companyName: "StartupVentures",
    location: "Delhi, Mumbai, Bangalore, Pune",
    duration: 2,
    stipend: 10000,
    internType: ["Full time"],
    skills: ["Sales", "Communication", "Market Research", "Lead Generation", "CRM"],
    perks: ["Certificate", "Letter of recommendation", "Job offer", "Incentives"],
    hiringSince: "March 2024",
    openings: 5,
    applicants: 98,
    websiteLink: "https://startupventures.in",
    education: "Graduation"
  },
  {
    id: "2451137",
    role: "Content Writing Internship",
    companyName: "Content Creators Hub",
    location: "Remote",
    duration: 2,
    stipend: 8000,
    internType: ["Part time", "Work from home"],
    skills: ["Content Writing", "SEO Writing", "Blog Writing", "Creative Writing", "Research"],
    perks: ["Certificate", "Flexible work hours", "Work from home"],
    hiringSince: "September 2023",
    openings: 6,
    applicants: 212,
    websiteLink: "https://contentcreatorshub.com",
    education: "Graduation"
  },
  {
    id: "2448829",
    role: "Mobile App Development Internship",
    companyName: "AppCraft Technologies",
    location: "Bangalore, Hyderabad, Chennai, Pune",
    duration: 4,
    stipend: 22000,
    internType: ["Full time"],
    skills: ["React Native", "Flutter", "JavaScript", "Firebase", "Mobile UI Design"],
    perks: ["Certificate", "Letter of recommendation", "Job offer", "Team outings"],
    hiringSince: "November 2023",
    openings: 2,
    applicants: 134,
    websiteLink: "https://appcraft.tech",
    education: "Graduation"
  },
  {
    id: "2453422",
    role: "Artificial Intelligence Internship",
    companyName: "AI Innovations Lab",
    location: "Bangalore, Delhi, Mumbai, Hyderabad",
    duration: 6,
    stipend: 30000,
    internType: ["Full time"],
    skills: ["Python", "TensorFlow", "PyTorch", "Computer Vision", "Natural Language Processing", "Deep Learning"],
    perks: ["Certificate", "Letter of recommendation", "Job offer", "Health insurance", "5 days a week"],
    hiringSince: "April 2023",
    openings: 1,
    applicants: 289,
    websiteLink: "https://aiinnovations.lab",
    education: "Graduation"
  },
  {
    id: "2452150",
    role: "Cloud Computing Internship",
    companyName: "CloudTech Solutions",
    location: "Bangalore, Hyderabad, Pune, Chennai",
    duration: 3,
    stipend: 20000,
    internType: ["Full time"],
    skills: ["AWS", "Azure", "Docker", "Kubernetes", "Linux", "DevOps"],
    perks: ["Certificate", "Letter of recommendation", "Training & Development"],
    hiringSince: "September 2023",
    openings: 3,
    applicants: 176,
    websiteLink: "https://cloudtechsolutions.io",
    education: "Graduation"
  },
  {
    id: "2461234",
    role: "Blockchain Development Internship",
    companyName: "CryptoTech Innovations",
    location: "Bangalore, Mumbai, Delhi",
    duration: 4,
    stipend: 28000,
    internType: ["Full time", "Remote"],
    skills: ["Solidity", "Web3.js", "Ethereum", "Smart Contracts", "JavaScript", "React"],
    perks: ["Certificate", "Letter of recommendation", "Remote work", "Performance bonus"],
    hiringSince: "January 2024",
    openings: 2,
    applicants: 143,
    websiteLink: "https://cryptotech.innovations",
    education: "Graduation"
  },
  {
    id: "2461567",
    role: "Cybersecurity Internship",
    companyName: "SecureNet Systems",
    location: "Delhi, Bangalore, Mumbai, Hyderabad",
    duration: 3,
    stipend: 18000,
    internType: ["Full time"],
    skills: ["Network Security", "Ethical Hacking", "Python", "Linux", "Penetration Testing"],
    perks: ["Certificate", "Letter of recommendation", "Training & Development"],
    hiringSince: "February 2024",
    openings: 2,
    applicants: 165,
    websiteLink: "https://securenet.systems",
    education: "Graduation"
  },
  {
    id: "2461890",
    role: "Product Management Internship",
    companyName: "ProductLabs",
    location: "Bangalore, Mumbai, Delhi",
    duration: 3,
    stipend: 15000,
    internType: ["Full time"],
    skills: ["Product Strategy", "Market Research", "Data Analysis", "Agile", "User Research"],
    perks: ["Certificate", "Letter of recommendation", "5 days a week", "Team outings"],
    hiringSince: "March 2024",
    openings: 2,
    applicants: 187,
    websiteLink: "https://productlabs.io",
    education: "Graduation"
  },
  {
    id: "2462123",
    role: "Game Development Internship",
    companyName: "GameStudio Pro",
    location: "Bangalore, Mumbai, Pune",
    duration: 4,
    stipend: 16000,
    internType: ["Full time"],
    skills: ["Unity", "C#", "Game Design", "3D Modeling", "Animation"],
    perks: ["Certificate", "Letter of recommendation", "Informal dress code", "Free snacks"],
    hiringSince: "April 2024",
    openings: 2,
    applicants: 124,
    websiteLink: "https://gamestudio.pro",
    education: "Graduation"
  },
  {
    id: "2462456",
    role: "HR Management Internship",
    companyName: "TalentBridge Consulting",
    location: "Mumbai, Delhi, Bangalore, Chennai",
    duration: 2,
    stipend: 10000,
    internType: ["Full time"],
    skills: ["Recruitment", "MS Excel", "Communication", "HR Policies", "Employee Relations"],
    perks: ["Certificate", "Letter of recommendation", "5 days a week"],
    hiringSince: "May 2024",
    openings: 3,
    applicants: 156,
    websiteLink: "https://talentbridge.consulting",
    education: "Graduation"
  }
];

// Helper functions for data processing
export const getUniqueLocations = (): string[] => {
  const locations = new Set<string>();
  mockInternships.forEach(internship => {
    internship.location.split(',').forEach(loc => {
      locations.add(loc.trim());
    });
  });
  return Array.from(locations).sort();
};

export const getUniqueSkills = (): string[] => {
  const skills = new Set<string>();
  mockInternships.forEach(internship => {
    internship.skills.forEach(skill => skills.add(skill));
  });
  return Array.from(skills).sort();
};

export const getUniquePerks = (): string[] => {
  const perks = new Set<string>();
  mockInternships.forEach(internship => {
    internship.perks.forEach(perk => perks.add(perk));
  });
  return Array.from(perks).sort();
};