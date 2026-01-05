/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  allowedDevOrigins: [
    'http://localhost:9002',
    'http://127.0.0.1:9002',
    'http://192.168.4.28:9002',
  ],
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: '127.0.0.1' },
      { protocol: 'http', hostname: '192.168.4.28' },
    ],
  },
};

export default nextConfig;

