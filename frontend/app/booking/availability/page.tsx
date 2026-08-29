import { Metadata } from 'next';
import AvailabilityCalendar from '@/components/booking/AvailabilityCalendar';
import ServiceSelector from '@/components/booking/ServiceSelector';

export const metadata: Metadata = {
  title: 'Check Availability - Nkubu Garage',
  description: 'View available booking slots for our services.',
};

export default function AvailabilityPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Check Availability</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <ServiceSelector />
        </div>
        <div className="lg:col-span-2">
          <AvailabilityCalendar />
        </div>
      </div>
    </div>
  );
}
