import GlobalStyle from "./globalStyle";
import Head from "next/head";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head></Head>
      <GlobalStyle />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
