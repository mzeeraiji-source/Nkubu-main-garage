import { Metadata } from 'next';
import TeamSection from '@/components/garage/TeamSection';
import StorySection from '@/components/garage/StorySection';
import ValuesSection from '@/components/garage/ValuesSection';
import AwardsSection from '@/components/garage/AwardsSection';

export const metadata: Metadata = {
  title: 'About Us - Nkubu Garage',
  description: 'Learn about Nkubu Garage and our commitment to automotive excellence.',
};

export default function AboutPage() {
  return (
    <div className="space-y-16">
      <StorySection />
      <ValuesSection />
      <TeamSection />
      <AwardsSection />
    </div>
  );
}
