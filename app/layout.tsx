import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mizan Investments",
  description: "Shariah-compliant stock screening & analysis",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="antialiased">
      <body className="min-h-screen font-body">{children}</body>
    </html>
  );
}
