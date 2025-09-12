import { ScoredInternship } from '@/utils/internshipMatcher';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { 
  MapPin, 
  Calendar, 
  DollarSign, 
  Users, 
  Building2, 
  ExternalLink,
  Sparkles,
  Trophy,
  TrendingUp
} from 'lucide-react';
import { getMatchLevel } from '@/utils/internshipMatcher';

interface InternshipCardProps {
  internship: ScoredInternship;
  isTopMatch?: boolean;
}

export const InternshipCard = ({ internship, isTopMatch = false }: InternshipCardProps) => {
  const matchLevel = getMatchLevel(internship.matchScore);
  
  return (
    <Card className={`
      relative overflow-hidden transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl
      bg-card/80 backdrop-blur-sm border-border/50
      ${isTopMatch ? 'ring-2 ring-accent shadow-gold' : ''}
    `}>
      {isTopMatch && (
        <div className="absolute top-0 right-0 p-3">
          <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-gradient-accent text-accent-foreground text-sm font-semibold">
            <Trophy className="h-4 w-4" />
            Top Match
          </div>
        </div>
      )}
      
      <div className="p-6 space-y-4">
        {/* Header */}
        <div className="space-y-2">
          <h3 className="text-xl font-bold text-foreground flex items-center gap-2">
            {internship.role}
            {internship.matchScore >= 80 && <Sparkles className="h-5 w-5 text-accent" />}
          </h3>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Building2 className="h-4 w-4" />
            <span className="font-medium">{internship.companyName}</span>
          </div>
        </div>

        {/* Key Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground truncate">{internship.location}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <DollarSign className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground">₹{internship.stipend.toLocaleString()}/month</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Calendar className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground">{internship.duration} months</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Users className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground">{internship.applicants} applicants</span>
          </div>
        </div>

        {/* Skills */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">Required Skills</p>
          <div className="flex flex-wrap gap-2">
            {internship.skills.slice(0, 5).map((skill, index) => (
              <Badge key={index} variant="secondary" className="bg-badge-skill/20 text-foreground border-badge-skill/30">
                {skill}
              </Badge>
            ))}
            {internship.skills.length > 5 && (
              <Badge variant="outline" className="text-muted-foreground">
                +{internship.skills.length - 5} more
              </Badge>
            )}
          </div>
        </div>

        {/* Perks */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">Perks & Benefits</p>
          <div className="flex flex-wrap gap-2">
            {internship.perks.map((perk, index) => (
              <Badge key={index} variant="secondary" className="bg-badge-perk/20 text-foreground border-badge-perk/30">
                {perk}
              </Badge>
            ))}
          </div>
        </div>

        {/* Match Score */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-muted-foreground">Match Score</span>
            <span className={`text-sm font-bold ${matchLevel.color}`}>
              {Math.round(internship.matchScore)}% • {matchLevel.label}
            </span>
          </div>
          <div className="relative h-2 bg-muted rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all duration-500 ${matchLevel.bgColor}`}
              style={{ width: `${internship.matchScore}%` }}
            />
          </div>
          
          {/* Match Details */}
          <div className="flex gap-4 text-xs text-muted-foreground pt-1">
            {internship.skillMatchRatio > 0 && (
              <div className="flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                {Math.round(internship.skillMatchRatio * 100)}% skill match
              </div>
            )}
            {internship.locationMatch && (
              <div className="flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                Location match
              </div>
            )}
            {internship.stipendMatch && (
              <div className="flex items-center gap-1">
                <DollarSign className="h-3 w-3" />
                Meets stipend requirement
              </div>
            )}
          </div>
        </div>

        {/* Apply Button */}
        {internship.websiteLink && (
          <Button 
            className="w-full bg-gradient-primary hover:opacity-90 transition-all"
            asChild
          >
            <a 
              href={internship.websiteLink} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2"
            >
              Apply Now
              <ExternalLink className="h-4 w-4" />
            </a>
          </Button>
        )}
      </div>
    </Card>
  );
};