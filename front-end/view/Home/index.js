import { useState } from "react";
import styled from "styled-components";

import style from "./style";

const Home = ({ className }) => {
  const [activeTab, setActiveTab] = useState("questions");

  const questions = [
    { id: 1, name: "Reverse String", link: "/questions/reverse-string" },
    {
      id: 2,
      name: "Fibonacci Sequence",
      link: "/questions/fibonacci-sequence"
    },
    { id: 3, name: "Binary Search", link: "/questions/binary-search" },
    {
      id: 4,
      name: "Merge Two Sorted Arrays",
      link: "/questions/merge-sorted-arrays"
    },
    { id: 5, name: "Palindrome Number", link: "/questions/palindrome-number" }
  ];

  const rankings = [
    { username: "JohnDoe", score: 950 },
    { username: "AliceSmith", score: 920 },
    { username: "BobJohnson", score: 890 },
    { username: "EmmaDavis", score: 860 },
    { username: "MichaelWilson", score: 830 },
    { username: "SophiaBrown", score: 800 },
    { username: "DavidLee", score: 770 },
    { username: "OliviaMartin", score: 740 },
    { username: "JamesAnderson", score: 710 },
    { username: "EmilyTaylor", score: 680 }
  ];

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
            <div className="coach-container">
              <div className="tabs">
                <button
                  className={activeTab === "questions" ? "active" : ""}
                  onClick={() => setActiveTab("questions")}
                >
                  Questions
                </button>
                <button
                  className={activeTab === "ranking" ? "active" : ""}
                  onClick={() => setActiveTab("ranking")}
                >
                  Ranking
                </button>
              </div>
              <div className="tab-content">
                {activeTab === "questions" && (
                  <ul>
                    {questions.map((q) => (
                      <li key={q.id}>
                        <a href={q.link}>
                          {q.id}. {q.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
                {activeTab === "ranking" && (
                  <ul className="ranking-list">
                    {rankings.map((r, index) => (
                      <li
                        key={index}
                        className={index < 3 ? `top-${index + 1}` : ""}
                      >
                        <span className="rank">{index + 1}</span>
                        <span className="username">{r.username}</span>
                        <span className="score">{r.score}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default styled(Home)`
  ${style}
`;
