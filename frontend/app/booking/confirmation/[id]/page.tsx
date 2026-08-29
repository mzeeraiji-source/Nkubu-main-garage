import { Metadata } from 'next';
import BookingConfirmation from '@/components/booking/BookingConfirmation';
import NextSteps from '@/components/booking/NextSteps';

interface ConfirmationPageProps {
  params: {
    id: string;
  };
}

export const metadata: Metadata = {
  title: 'Booking Confirmed - Nkubu Garage',
  description: 'Your booking has been confirmed',
};

export default function ConfirmationPage({ params }: ConfirmationPageProps) {
  return (
    <div className="container mx-auto px-4 py-12">
      <BookingConfirmation bookingId={params.id} />
      <NextSteps />
    </div>
  );
}
