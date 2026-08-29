import { Metadata } from 'next';
import CheckoutForm from '@/components/shop/CheckoutForm';
import OrderSummary from '@/components/shop/OrderSummary';

export const metadata: Metadata = {
  title: 'Checkout - Nkubu Garage',
  description: 'Complete your purchase at Nkubu Garage',
};

export default function CheckoutPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Checkout</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <CheckoutForm />
        </div>
        <OrderSummary />
      </div>
    </div>
  );
}
