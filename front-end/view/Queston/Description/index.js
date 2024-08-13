import styled from "styled-components";
import style from "./style";

const Description = ({ description, title, className }) => (
  <div className={className}>
    <h1>{title}</h1>
    <div dangerouslySetInnerHTML={{ __html: description }} />
  </div>
);

export default styled(Description)`
  ${style}
`;
