import { Metadata } from 'next';
import ServiceDetail from '@/components/garage/ServiceDetail';
import RelatedServices from '@/components/garage/RelatedServices';
import BookingCTA from '@/components/garage/BookingCTA';

interface ServicePageProps {
  params: {
    slug: string;
  };
}

export async function generateMetadata({
  params,
}: ServicePageProps): Promise<Metadata> {
  return {
    title: `${params.slug.replace(/-/g, ' ')} - Nkubu Garage`,
    description: 'Get expert automotive service at Nkubu Garage',
  };
}

export default function ServicePage({ params }: ServicePageProps) {
  return (
    <div className="container mx-auto px-4 py-12">
      <ServiceDetail slug={params.slug} />
      <BookingCTA serviceSlug={params.slug} />
      <RelatedServices currentSlug={params.slug} />
    </div>
  );
}
