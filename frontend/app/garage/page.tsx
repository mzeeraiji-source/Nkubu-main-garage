import { Metadata } from 'next';
import GarageOverview from '@/components/garage/GarageOverview';
import ServiceMenu from '@/components/garage/ServiceMenu';
import Testimonials from '@/components/garage/Testimonials';
import Gallery from '@/components/garage/Gallery';

export const metadata: Metadata = {
  title: 'Our Garage - Nkubu',
  description: 'Explore our professional automotive workshop with AI-powered diagnostics.',
};

export default function GaragePage() {
  return (
    <div className="space-y-16">
      <GarageOverview />
      <ServiceMenu />
      <Gallery />
      <Testimonials />
    </div>
  );
}
