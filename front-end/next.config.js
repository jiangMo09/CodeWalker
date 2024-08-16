/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  reactStrictMode: false,
  compiler: {
    styledComponents: true
  },
  experimental: {
    esmExternals: false
  }
};

module.exports = nextConfig;
