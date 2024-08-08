import { useState } from "react";
import styled from "styled-components";

import style from "./style";

const Home = ({ className }) => {
  return (
    <div className={className}>
      <div className="website-name">CodeWalker</div>
      <div className="main">
        <div className="description">
          CodeWalker, your coach and partner, coding together, getting stronger.
        </div>
        <div className="features">
          <div className="feature">
            <div className="title">deployment partner</div>
            <div className="feature-description">
              <ul>
                <li>
                  Projects can be deployed via public GitHub repository links.
                </li>
                <li>The project type must be pure JavaScript.</li>
              </ul>
            </div>
            <div className="entry">go to deploying</div>
          </div>
          <div className="feature">
            <div className="title">coding coach</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default styled(Home)`
  ${style}
`;
