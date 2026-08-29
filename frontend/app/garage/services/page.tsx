import { Metadata } from 'next';
import ServiceCatalog from '@/components/garage/ServiceCatalog';
import ServiceFilters from '@/components/garage/ServiceFilters';

export const metadata: Metadata = {
  title: 'Services - Nkubu Garage',
  description: 'Browse our comprehensive automotive service offerings.',
};

export default function ServicesPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">Our Services</h1>
      <p className="text-lg text-gray-600 mb-8">
        Professional automotive services backed by AI diagnostics and expert technicians
      </p>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <ServiceFilters />
        <div className="lg:col-span-3">
          <ServiceCatalog />
        </div>
      </div>
    </div>
  );
}
