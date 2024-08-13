import styled from "styled-components";
import style from "./style";

const Header = ({ className }) => {
  return (
    <div className={className}>
      <div className="logo">CodeWalker</div>
      <div className="buttons">
        <div className="button run">
          <img className="run-icon icon" src="/images/run.svg" />
          run
        </div>
        <div className="button submit">
          <img
            className="cloud-arrow-up-icon icon"
            src="/images/cloud-arrow-up.svg"
          />
          submit
        </div>
      </div>
      <div className="user">user : Leona</div>
    </div>
  );
};

export default styled(Header)`
  ${style}
`;
