import { Metadata } from 'next';
import ContactForm from '@/components/garage/ContactForm';
import LocationMap from '@/components/garage/LocationMap';
import BusinessHours from '@/components/garage/BusinessHours';

export const metadata: Metadata = {
  title: 'Contact Us - Nkubu Garage',
  description: 'Get in touch with Nkubu Garage for inquiries and support.',
};

export default function ContactPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-12">
        <div className="lg:col-span-2">
          <ContactForm />
        </div>
        <div className="space-y-8">
          <LocationMap />
          <BusinessHours />
        </div>
      </div>
    </div>
  );
}
