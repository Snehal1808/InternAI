import { Internship } from '@/data/mockInternships';

export interface CandidateProfile {
  locations: string[];
  skills: string[];
  education: string;
  minStipend: number;
}

export interface ScoredInternship extends Internship {
  matchScore: number;
  skillMatchRatio: number;
  locationMatch: boolean;
  stipendMatch: boolean;
}

// Calculate skill match ratio
const calculateSkillMatch = (internshipSkills: string[], candidateSkills: string[]): number => {
  if (candidateSkills.length === 0) return 0.5; // Default score if no skills specified
  
  const internshipSkillsLower = internshipSkills.map(s => s.toLowerCase());
  const matchingSkills = candidateSkills.filter(skill => 
    internshipSkillsLower.some(iSkill => 
      iSkill.includes(skill.toLowerCase()) || skill.toLowerCase().includes(iSkill)
    )
  );
  
  return matchingSkills.length / candidateSkills.length;
};

// Check location match
const checkLocationMatch = (internshipLocation: string, candidateLocations: string[]): boolean => {
  if (candidateLocations.length === 0) return true; // All locations if none specified
  if (internshipLocation.toLowerCase().includes('remote')) return true;
  
  const internshipLocationsLower = internshipLocation.toLowerCase();
  return candidateLocations.some(loc => 
    internshipLocationsLower.includes(loc.toLowerCase())
  );
};

// Calculate overall match score
const calculateMatchScore = (
  internship: Internship,
  profile: CandidateProfile,
  skillMatchRatio: number,
  locationMatch: boolean,
  stipendMatch: boolean
): number => {
  let score = 0;
  
  // Skill match weight: 40%
  score += skillMatchRatio * 40;
  
  // Location match weight: 20%
  if (locationMatch) score += 20;
  
  // Stipend weight: 25%
  if (stipendMatch) {
    const stipendBonus = Math.min((internship.stipend / 50000) * 25, 25);
    score += stipendBonus;
  }
  
  // Duration weight: 10% (prefer 3-4 month internships)
  const idealDuration = internship.duration >= 3 && internship.duration <= 4;
  if (idealDuration) score += 10;
  else if (internship.duration >= 2 && internship.duration <= 6) score += 5;
  
  // Perks weight: 5%
  const hasGoodPerks = internship.perks.some(perk => 
    ['Job offer', 'Letter of recommendation', 'Certificate', 'Performance bonus'].includes(perk)
  );
  if (hasGoodPerks) score += 5;
  
  return Math.min(score, 100);
};

// Main matching function
export const matchInternships = (
  internships: Internship[],
  profile: CandidateProfile
): ScoredInternship[] => {
  const scoredInternships: ScoredInternship[] = internships.map(internship => {
    const skillMatchRatio = calculateSkillMatch(internship.skills, profile.skills);
    const locationMatch = checkLocationMatch(internship.location, profile.locations);
    const stipendMatch = internship.stipend >= profile.minStipend;
    
    const matchScore = calculateMatchScore(
      internship,
      profile,
      skillMatchRatio,
      locationMatch,
      stipendMatch
    );
    
    return {
      ...internship,
      matchScore,
      skillMatchRatio,
      locationMatch,
      stipendMatch
    };
  });
  
  // Filter out internships with very low match scores
  return scoredInternships
    .filter(internship => 
      internship.matchScore >= 20 && // Minimum 20% match
      (profile.skills.length === 0 || internship.skillMatchRatio > 0) // Has some skill match if skills specified
    )
    .sort((a, b) => b.matchScore - a.matchScore);
};

// Get match level based on score
export const getMatchLevel = (score: number): {
  label: string;
  color: string;
  bgColor: string;
} => {
  if (score >= 80) return { 
    label: 'Excellent Match', 
    color: 'text-green-400',
    bgColor: 'bg-gradient-to-r from-green-500 to-emerald-500'
  };
  if (score >= 60) return { 
    label: 'Good Match', 
    color: 'text-yellow-400',
    bgColor: 'bg-gradient-to-r from-yellow-500 to-amber-500'
  };
  if (score >= 40) return { 
    label: 'Fair Match', 
    color: 'text-orange-400',
    bgColor: 'bg-gradient-to-r from-orange-500 to-orange-600'
  };
  return { 
    label: 'Low Match', 
    color: 'text-red-400',
    bgColor: 'bg-gradient-to-r from-red-500 to-red-600'
  };
};