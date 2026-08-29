'use client';

import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';
import VehiclesList from '@/components/account/VehiclesList';
import AddVehicleModal from '@/components/account/AddVehicleModal';

export default function VehiclesPage() {
  const { data: session } = useSession();

  if (!session) {
    redirect('/auth/signin');
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">My Vehicles</h1>
        <AddVehicleModal />
      </div>
      <VehiclesList />
    </div>
  );
}
