import { Metadata } from 'next';
import BookingWizard from '@/components/booking/BookingWizard';

export const metadata: Metadata = {
  title: 'Book Service - Nkubu Garage',
  description: 'Book your automotive service with Nkubu Garage',
};

export default function BookingPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">Book Your Service</h1>
      <p className="text-lg text-gray-600 mb-8">
        Schedule your appointment in just a few clicks
      </p>
      <BookingWizard />
    </div>
  );
}
