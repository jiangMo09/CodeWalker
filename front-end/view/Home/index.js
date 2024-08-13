import { useState, useEffect } from "react";
import styled from "styled-components";
import { getQuestionsList } from "../../services/api/Home";

import style from "./style";

const Home = ({ className }) => {
  const [activeTab, setActiveTab] = useState("questions");
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    const getQuestions = async () => {
      try {
        const questionsList = await getQuestionsList();
        if (questionsList && questionsList.questions) {
          setQuestions(questionsList.questions);
        }
      } catch (error) {
        console.error("Failed to fetch questions:", error);
      }
    };

    getQuestions();
  }, []);

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
            <div className="title">Deployment Partner</div>
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
            <div className="title">Coding Coach</div>
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
                        <a href={`/question/${q.kebab_case_name}`}>
                          {q.id}. {q.pretty_name}
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
