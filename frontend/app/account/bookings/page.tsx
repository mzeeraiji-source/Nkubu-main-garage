'use client';

import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';
import BookingsList from '@/components/account/BookingsList';
import BookingFilters from '@/components/account/BookingFilters';

export default function BookingsPage() {
  const { data: session } = useSession();

  if (!session) {
    redirect('/auth/signin');
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">My Bookings</h1>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <BookingFilters />
        <div className="lg:col-span-3">
          <BookingsList />
        </div>
      </div>
    </div>
  );
}
