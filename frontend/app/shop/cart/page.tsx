import { Metadata } from 'next';
import ShoppingCart from '@/components/shop/ShoppingCart';
import CartSummary from '@/components/shop/CartSummary';

export const metadata: Metadata = {
  title: 'Shopping Cart - Nkubu Garage',
  description: 'Review your shopping cart',
};

export default function CartPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Shopping Cart</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <ShoppingCart />
        </div>
        <CartSummary />
      </div>
    </div>
  );
}
