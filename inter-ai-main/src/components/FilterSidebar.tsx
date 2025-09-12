import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Search, 
  MapPin, 
  Code, 
  GraduationCap, 
  DollarSign,
  Filter,
  Sparkles
} from 'lucide-react';
import { CandidateProfile } from '@/utils/internshipMatcher';

interface FilterSidebarProps {
  availableLocations: string[];
  availableSkills: string[];
  onSearch: (profile: CandidateProfile) => void;
}

export const FilterSidebar = ({ 
  availableLocations, 
  availableSkills, 
  onSearch 
}: FilterSidebarProps) => {
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [education, setEducation] = useState<string>('Graduation');
  const [minStipend, setMinStipend] = useState<number>(0);
  const [skillSearchTerm, setSkillSearchTerm] = useState('');
  const [locationSearchTerm, setLocationSearchTerm] = useState('');

  const handleLocationToggle = (location: string) => {
    setSelectedLocations(prev => 
      prev.includes(location) 
        ? prev.filter(l => l !== location)
        : [...prev, location]
    );
  };

  const handleSkillToggle = (skill: string) => {
    setSelectedSkills(prev => 
      prev.includes(skill) 
        ? prev.filter(s => s !== skill)
        : [...prev, skill]
    );
  };

  const handleSearch = () => {
    onSearch({
      locations: selectedLocations,
      skills: selectedSkills,
      education,
      minStipend
    });
  };

  const filteredLocations = availableLocations.filter(loc =>
    loc.toLowerCase().includes(locationSearchTerm.toLowerCase())
  );

  const filteredSkills = availableSkills.filter(skill =>
    skill.toLowerCase().includes(skillSearchTerm.toLowerCase())
  );

  return (
    <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50 sticky top-4">
      <div className="space-y-6">
        <div className="flex items-center gap-2">
          <Filter className="h-5 w-5 text-primary" />
          <h2 className="text-xl font-bold text-foreground">Filters</h2>
        </div>

        {/* Education Level */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <GraduationCap className="h-4 w-4 text-primary" />
            <Label className="text-foreground">Education Level</Label>
          </div>
          <select 
            value={education}
            onChange={(e) => setEducation(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-input border border-border text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="Class 10">Class 10</option>
            <option value="Class 12">Class 12</option>
            <option value="Diploma">Diploma</option>
            <option value="Graduation">Graduation</option>
            <option value="Post Graduation">Post Graduation</option>
          </select>
        </div>

        {/* Minimum Stipend */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-primary" />
              <Label className="text-foreground">Minimum Stipend</Label>
            </div>
            <span className="text-sm font-medium text-primary">
              ₹{minStipend.toLocaleString()}/month
            </span>
          </div>
          <Slider
            value={[minStipend]}
            onValueChange={(value) => setMinStipend(value[0])}
            min={0}
            max={50000}
            step={1000}
            className="w-full"
          />
        </div>

        {/* Locations */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4 text-primary" />
            <Label className="text-foreground">Preferred Locations</Label>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search locations..."
              value={locationSearchTerm}
              onChange={(e) => setLocationSearchTerm(e.target.value)}
              className="w-full pl-10 pr-3 py-2 rounded-lg bg-input border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <ScrollArea className="h-32 rounded-lg border border-border/50 p-2">
            <div className="space-y-2">
              {filteredLocations.map(location => (
                <div key={location} className="flex items-center space-x-2">
                  <Checkbox
                    id={`loc-${location}`}
                    checked={selectedLocations.includes(location)}
                    onCheckedChange={() => handleLocationToggle(location)}
                  />
                  <label
                    htmlFor={`loc-${location}`}
                    className="text-sm text-foreground cursor-pointer hover:text-primary transition-colors"
                  >
                    {location}
                  </label>
                </div>
              ))}
            </div>
          </ScrollArea>
          {selectedLocations.length > 0 && (
            <div className="text-xs text-muted-foreground">
              {selectedLocations.length} location(s) selected
            </div>
          )}
        </div>

        {/* Skills */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Code className="h-4 w-4 text-primary" />
            <Label className="text-foreground">Skills</Label>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search skills..."
              value={skillSearchTerm}
              onChange={(e) => setSkillSearchTerm(e.target.value)}
              className="w-full pl-10 pr-3 py-2 rounded-lg bg-input border border-border text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <ScrollArea className="h-32 rounded-lg border border-border/50 p-2">
            <div className="space-y-2">
              {filteredSkills.map(skill => (
                <div key={skill} className="flex items-center space-x-2">
                  <Checkbox
                    id={`skill-${skill}`}
                    checked={selectedSkills.includes(skill)}
                    onCheckedChange={() => handleSkillToggle(skill)}
                  />
                  <label
                    htmlFor={`skill-${skill}`}
                    className="text-sm text-foreground cursor-pointer hover:text-primary transition-colors"
                  >
                    {skill}
                  </label>
                </div>
              ))}
            </div>
          </ScrollArea>
          {selectedSkills.length > 0 && (
            <div className="text-xs text-muted-foreground">
              {selectedSkills.length} skill(s) selected
            </div>
          )}
        </div>

        {/* Search Button */}
        <Button 
          onClick={handleSearch}
          className="w-full bg-gradient-primary hover:opacity-90 transition-all"
        >
          <Sparkles className="h-4 w-4 mr-2" />
          Get AI Recommendations
        </Button>
      </div>
    </Card>
  );
};