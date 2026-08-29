import { Metadata } from 'next';
import ShopHero from '@/components/shop/ShopHero';
import ProductGrid from '@/components/shop/ProductGrid';
import CategoryFilter from '@/components/shop/CategoryFilter';
import Promotions from '@/components/shop/Promotions';

export const metadata: Metadata = {
  title: 'Shop - Nkubu Garage',
  description: 'Browse automotive parts and accessories from Nkubu Garage',
};

export default function ShopPage() {
  return (
    <>
      <ShopHero />
      <Promotions />
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <CategoryFilter />
          <div className="lg:col-span-3">
            <ProductGrid />
          </div>
        </div>
      </div>
    </>
  );
}
