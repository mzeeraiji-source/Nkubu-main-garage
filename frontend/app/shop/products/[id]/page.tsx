import { Metadata } from 'next';
import ProductDetail from '@/components/shop/ProductDetail';
import RelatedProducts from '@/components/shop/RelatedProducts';
import Reviews from '@/components/shop/Reviews';

interface ProductPageProps {
  params: {
    id: string;
  };
}

export async function generateMetadata({
  params,
}: ProductPageProps): Promise<Metadata> {
  return {
    title: 'Product - Nkubu Garage Shop',
    description: 'Browse automotive parts at Nkubu Garage',
  };
}

export default function ProductPage({ params }: ProductPageProps) {
  return (
    <div className="container mx-auto px-4 py-12">
      <ProductDetail productId={params.id} />
      <Reviews productId={params.id} />
      <RelatedProducts productId={params.id} />
    </div>
  );
}
