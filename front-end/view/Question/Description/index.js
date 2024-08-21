import styled from "styled-components";
import style from "./style";

const Description = ({ description, title, className }) => (
  <div className={`${className} description`}>
    {/* <div className="description"> */}
      <h1>{title}</h1>
      <div dangerouslySetInnerHTML={{ __html: description }} />
    {/* </div> */}
  </div>
);

export default styled(Description)`
  ${style}
`;
