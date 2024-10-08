import { useState, useEffect } from "react";
import styled from "styled-components";
import { getQuestionsList, getRanking } from "../../services/api/Home";

import User from "../User";
import style from "./style";

const Home = ({ className }) => {
  const [activeTab, setActiveTab] = useState("questions");
  const [questions, setQuestions] = useState([]);
  const [rankings, setRankings] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const questionsList = await getQuestionsList();
        if (questionsList && questionsList.questions) {
          setQuestions(questionsList.questions);
        }

        const rankingData = await getRanking();
        if (rankingData) {
          setRankings(rankingData);
        }
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className={className}>
      <div className="header">
        <div></div>
        <div className="website-name">CodeWalker</div>
        <User />
      </div>
      <div className="main">
        <div className="description">
          CodeWalker, your coach and partner, coding together, getting stronger.
        </div>
        <div className="features">
          <div className="feature">
            <div className="title">
              <div className="triangle-up" />
              Deployment Partner
            </div>
            <div className="feature-description">
              <ul>
                <li>
                  Projects can be deployed via public GitHub repository links.
                </li>
                <li>The project type must be pure JavaScript.</li>
              </ul>
            </div>
            <a className="entry" href="/deploy">
              go to deploying
            </a>
          </div>
          <div className="feature">
            <div className="title">
              <img
                className="coding-logo"
                src="https://leetcode.com/_next/static/images/logo-dark-c96c407d175e36c81e236fcfdd682a0b.png"
              />
              Coding Coach
            </div>
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
