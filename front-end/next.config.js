/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  reactStrictMode: true,
  compiler: {
    styledComponents: true
  },
  experimental: {
    esmExternals: false
  }
};

module.exports = nextConfig;
