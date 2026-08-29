import type { Metadata } from 'next';
import { Providers } from '@/app/providers';
import Navigation from '@/components/Navigation';
import Footer from '@/components/Footer';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'Nkubu Garage - AI-Powered Automotive Workshop',
  description: 'Professional automotive service with AI diagnostics, online booking, and e-commerce.',
  keywords: [
    'auto repair',
    'car service',
    'automotive workshop',
    'AI diagnostics',
    'online booking',
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>
        <Providers>
          <Navigation />
          <main className="min-h-screen">{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
