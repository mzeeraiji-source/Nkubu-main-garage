import { Metadata } from 'next';
import SignInForm from '@/components/auth/SignInForm';
import SocialAuth from '@/components/auth/SocialAuth';

export const metadata: Metadata = {
  title: 'Sign In - Nkubu Garage',
  description: 'Sign in to your Nkubu Garage account',
};

export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Sign in to Nkubu</h2>
          <p className="mt-2 text-sm text-gray-600">Manage your bookings and orders</p>
        </div>
        <SignInForm />
        <SocialAuth />
      </div>
    </div>
  );
}
