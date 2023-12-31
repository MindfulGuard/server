import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MindfulGuard',
  description: 'MindfulGuard web application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/static/mindfulguard logo.png" />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
