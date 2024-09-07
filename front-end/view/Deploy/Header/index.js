import styled from "styled-components";
import User from "../../User";
import style from "./style";

const Header = ({ className }) => (
  <header className={className}>
    <a href="/" className="logo">
      CodeWalker
    </a>
    <User />
  </header>
);

export default styled(Header)`
  ${style}
`;
