import { ScoredInternship } from '@/utils/internshipMatcher';
import { InternshipCard } from './InternshipCard';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  Filter, 
  TrendingUp,
  AlertCircle
} from 'lucide-react';

interface ResultsSectionProps {
  internships: ScoredInternship[];
  isLoading?: boolean;
  hasSearched: boolean;
}

export const ResultsSection = ({ 
  internships, 
  isLoading = false,
  hasSearched
}: ResultsSectionProps) => {
  if (!hasSearched) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-4">
        <div className="p-4 rounded-full bg-primary/10">
          <Search className="h-8 w-8 text-primary" />
        </div>
        <h3 className="text-xl font-semibold text-foreground">Ready to Find Your Perfect Match?</h3>
        <p className="text-muted-foreground text-center max-w-md">
          Use the filters on the left to specify your preferences and get AI-powered internship recommendations
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-96 rounded-lg bg-card/50 animate-pulse" />
        ))}
      </div>
    );
  }

  if (internships.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 space-y-4">
        <div className="p-4 rounded-full bg-destructive/10">
          <AlertCircle className="h-8 w-8 text-destructive" />
        </div>
        <h3 className="text-xl font-semibold text-foreground">No Matching Internships Found</h3>
        <p className="text-muted-foreground text-center max-w-md">
          Try adjusting your filters to broaden your search criteria
        </p>
      </div>
    );
  }

  const topMatches = internships.slice(0, 3);
  const otherMatches = internships.slice(3);

  return (
    <div className="space-y-8">
      {/* Results Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h2 className="text-2xl font-bold text-foreground">
            Your Matches
          </h2>
          <Badge variant="secondary" className="px-3 py-1">
            {internships.length} Results
          </Badge>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <TrendingUp className="h-4 w-4" />
          Sorted by match score
        </div>
      </div>

      {/* Top Matches */}
      {topMatches.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="h-px flex-1 bg-border" />
            <span className="text-sm font-medium text-muted-foreground px-3">
              🏆 Top Matches
            </span>
            <div className="h-px flex-1 bg-border" />
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {topMatches.map((internship, index) => (
              <InternshipCard 
                key={internship.id} 
                internship={internship}
                isTopMatch={index === 0}
              />
            ))}
          </div>
        </div>
      )}

      {/* Other Matches */}
      {otherMatches.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="h-px flex-1 bg-border" />
            <span className="text-sm font-medium text-muted-foreground px-3">
              Other Recommendations
            </span>
            <div className="h-px flex-1 bg-border" />
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {otherMatches.map((internship) => (
              <InternshipCard 
                key={internship.id} 
                internship={internship}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
