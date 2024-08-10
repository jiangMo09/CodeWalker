/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    compiler: {
      styledComponents: true,
    },
    experimental: {
      esmExternals: false
    }
  }
  
  module.exports = nextConfig