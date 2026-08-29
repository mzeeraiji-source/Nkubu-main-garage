'use client';

import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';
import AccountDashboard from '@/components/account/AccountDashboard';
import BookingHistory from '@/components/account/BookingHistory';
import OrderHistory from '@/components/account/OrderHistory';
import ProfileSettings from '@/components/account/ProfileSettings';

export default function AccountPage() {
  const { data: session } = useSession();

  if (!session) {
    redirect('/auth/signin');
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">My Account</h1>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <nav className="lg:col-span-1 bg-gray-50 rounded-lg p-6 h-fit">
          <ul className="space-y-4">
            <li><a href="#dashboard" className="text-blue-600 font-semibold">Dashboard</a></li>
            <li><a href="#profile" className="text-gray-600">Profile</a></li>
            <li><a href="#bookings" className="text-gray-600">Bookings</a></li>
            <li><a href="#orders" className="text-gray-600">Orders</a></li>
          </ul>
        </nav>
        <div className="lg:col-span-3 space-y-12">
          <AccountDashboard />
          <ProfileSettings />
          <BookingHistory />
          <OrderHistory />
        </div>
      </div>
    </div>
  );
}
