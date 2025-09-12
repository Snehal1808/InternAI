import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Sparkles, 
  TrendingUp, 
  Award, 
  Users,
  ChevronDown,
  Rocket
} from 'lucide-react';
import heroBg from '@/assets/hero-bg.jpg';

interface HeroSectionProps {
  onGetStarted: () => void;
}

export const HeroSection = ({ onGetStarted }: HeroSectionProps) => {
  return (
    <section className="relative min-h-[600px] flex items-center justify-center overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-secondary/20 to-accent/20 animate-gradient" />
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-secondary/10" />
      </div>
      
      <div className="relative z-10 container mx-auto px-4 py-20 text-center space-y-8">
        {/* Purple box with InternAI */}
        <div className="flex justify-center">
          <div className="bg-gradient-primary px-12 py-6 rounded-2xl shadow-glow">
            <h1 className="text-5xl md:text-7xl font-bold text-primary-foreground">
              InternAI
            </h1>
          </div>
        </div>
        
        {/* Badge */}
        <div className="flex justify-center">
          <Badge className="px-4 py-1.5 bg-card/80 backdrop-blur-sm text-foreground border border-border/50">
            <Rocket className="h-3 w-3 mr-2" />
            AI-Powered Matching
          </Badge>
        </div>
        
        {/* Main heading */}
        <div className="space-y-4">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground">
            Find Your Perfect Internship Match
          </h2>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
            Discover opportunities that align with your skills, location, and career goals using advanced AI matching
          </p>
        </div>
        
        {/* Stats */}
        <div className="flex flex-wrap justify-center gap-8 py-8">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-primary/10">
              <TrendingUp className="h-5 w-5 text-primary" />
            </div>
            <div className="text-left">
              <p className="text-2xl font-bold text-foreground">95%</p>
              <p className="text-sm text-muted-foreground">Match Accuracy</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-secondary/10">
              <Award className="h-5 w-5 text-secondary" />
            </div>
            <div className="text-left">
              <p className="text-2xl font-bold text-foreground">500+</p>
              <p className="text-sm text-muted-foreground">Top Companies</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-accent/10">
              <Users className="h-5 w-5 text-accent" />
            </div>
            <div className="text-left">
              <p className="text-2xl font-bold text-foreground">10K+</p>
              <p className="text-sm text-muted-foreground">Active Internships</p>
            </div>
          </div>
        </div>
        
        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button 
            size="lg"
            onClick={onGetStarted}
            className="bg-gradient-primary hover:opacity-90 text-primary-foreground px-8 py-6 text-lg"
          >
            <Sparkles className="h-5 w-5 mr-2" />
            Get Started
          </Button>
          
          <Button 
            size="lg"
            variant="outline"
            className="px-8 py-6 text-lg border-border hover:bg-card"
          >
            Learn More
          </Button>
        </div>
        
        {/* Scroll indicator */}
        <div className="pt-8 animate-bounce">
          <ChevronDown className="h-6 w-6 text-muted-foreground mx-auto" />
        </div>
      </div>
    </section>
  );
};