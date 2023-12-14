/** @type {import('next').NextConfig} */
module.exports = {
  typescript: {
    ignoreBuildErrors: true,
  },
  webpack: (config, { isServer }) => {
    // ...
    config.stats = {
      warnings: false,
      errors: false
    };
    // ...
    return config;
  },
  eslint: {
    // Enable additional customizations here
    ignoreDuringBuilds: true,
  },
};
