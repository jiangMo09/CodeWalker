import GlobalStyle from "./globalStyle";
import Head from "next/head";
import GlobalProvider from "../providers/GlobalProvider";

function MyApp({ Component, pageProps }) {
  return (
    <GlobalProvider>
      <Head></Head>
      <GlobalStyle />
      <Component {...pageProps} />
    </GlobalProvider>
  );
}

export default MyApp;
