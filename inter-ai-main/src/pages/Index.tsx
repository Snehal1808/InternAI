import { useState, useRef } from 'react';
import { HeroSection } from '@/components/HeroSection';
import { FilterSidebar } from '@/components/FilterSidebar';
import { ResultsSection } from '@/components/ResultsSection';
import { InternshipCard } from '@/components/InternshipCard';
import { CandidateProfile, matchInternships, ScoredInternship } from '@/utils/internshipMatcher';
import { mockInternships, getUniqueLocations, getUniqueSkills } from '@/data/mockInternships';
import { Card } from '@/components/ui/card';
import { Sparkles } from 'lucide-react';
import { ThemeToggle } from '@/components/ThemeToggle';

const Index = () => {
  const [recommendations, setRecommendations] = useState<ScoredInternship[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  const handleSearch = async (profile: CandidateProfile) => {
    setIsLoading(true);
    setHasSearched(true);
    
    // Simulate AI processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const matches = matchInternships(mockInternships, profile);
    setRecommendations(matches.slice(0, 10)); // Show top 10 matches
    setIsLoading(false);
    
    // Scroll to results
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleGetStarted = () => {
    resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-background">
      <ThemeToggle />
      {/* Hero Section */}
      <HeroSection onGetStarted={handleGetStarted} />
      
      {/* Main Content */}
      <div ref={resultsRef} className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-3">
            <FilterSidebar
              availableLocations={getUniqueLocations()}
              availableSkills={getUniqueSkills()}
              onSearch={handleSearch}
            />
          </div>
          
          {/* Results Area */}
          <div className="lg:col-span-9">
            <ResultsSection
              internships={recommendations}
              isLoading={isLoading}
              hasSearched={hasSearched}
            />
          </div>
        </div>
      </div>
      
      {/* Footer */}
      <footer className="border-t border-border/50 py-8 mt-20">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <span className="font-semibold text-foreground">InternAI</span>
              <span className="text-muted-foreground">© 2024</span>
            </div>
            
            <div className="flex gap-6 text-sm text-muted-foreground">
              <a href="#" className="hover:text-primary transition-colors">About</a>
              <a href="#" className="hover:text-primary transition-colors">Contact</a>
              <a href="#" className="hover:text-primary transition-colors">Privacy</a>
              <a href="#" className="hover:text-primary transition-colors">Terms</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
