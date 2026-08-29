import { Metadata } from 'next';
import ForgotPasswordForm from '@/components/auth/ForgotPasswordForm';

export const metadata: Metadata = {
  title: 'Forgot Password - Nkubu Garage',
  description: 'Reset your Nkubu Garage password',
};

export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900">Reset password</h2>
          <p className="mt-2 text-sm text-gray-600">Enter your email to receive a reset link</p>
        </div>
        <ForgotPasswordForm />
      </div>
    </div>
  );
}
