import { Metadata } from 'next';
import DiagnosticForm from '@/components/garage/DiagnosticForm';
import DiagnosticBenefits from '@/components/garage/DiagnosticBenefits';
import FAQ from '@/components/garage/DiagnosticFAQ';

export const metadata: Metadata = {
  title: 'AI Diagnostics - Nkubu Garage',
  description: 'AI-powered vehicle diagnostics using Claude AI technology.',
};

export default function DiagnosticsPage() {
  return (
    <div className="space-y-16">
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">AI-Powered Vehicle Diagnostics</h1>
          <p className="text-xl">Get instant insights into your vehicle's health using advanced AI</p>
        </div>
      </section>
      <div className="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-12">
        <DiagnosticForm />
        <DiagnosticBenefits />
      </div>
      <FAQ />
    </div>
  );
}
