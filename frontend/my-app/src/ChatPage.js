import React, { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import './ChatPage.css';
import background from './assets/startPageBackground.jpg';
import fullBackground from './assets/fullBackground.jpg';
import speakButton from './assets/speakButton.png';
import listeningButton from './assets/listeningButton.png';

function ChatPage() {
  const location = useLocation();
  const [showButton, setShowButton] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [responseText, setResponseText] = useState("");
  const [responseImage, setResponseImage] = useState("");
  const [responseAudio, setResponseAudio] = useState("");
  const [vocabularyWords, setVocabularyWords] = useState([]); // 用于存储 word1, word2, word3
  const recognitionRef = useRef(null);

  // 生成以 "user" 开头的随机用户 ID
  const generateUserId = () => {
    return `user${Math.floor(1000 + Math.random() * 9000)}`;
  };

  const userId = useRef(generateUserId()); // 使用 useRef 保持 userId 的稳定性

  const initialUserInput = useRef(location.state?.user_input || "Unknown");
  console.log("location.state:", location.state);

  const hasSentRequest = useRef(false);

  useEffect(() => {
    if (!hasSentRequest.current) {
      console.log("ChatPage 接收到的数据:", initialUserInput.current);
      sendToBackend(initialUserInput.current);
      hasSentRequest.current = true;
    }
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => setShowButton(true), 2000);
    return () => clearTimeout(timeout);
  }, []);

  useEffect(() => {
    if (!("webkitSpeechRecognition" in window)) {
      console.warn("当前浏览器不支持 Web 语音识别 API");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event) => {
      console.error("语音识别错误:", event.error);
      setIsListening(false);
    };

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      console.log("识别到的文本:", text); // 打印语音识别结果到控制台
      sendToBackend(text);
    };

    recognitionRef.current = recognition;
  }, []);

  const startListening = () => {
    if (!recognitionRef.current) {
      alert("当前浏览器不支持语音识别，请使用 Chrome");
      return;
    }
    recognitionRef.current.start();
  };

  const sendToBackend = async (text) => {
    const requestBody = {
      user_id: userId.current, // 使用生成的随机 user_id
      user_input: text,
    };

    try {
      console.log("即将发送到后端的文本:", requestBody);
      const response = await fetch("http://localhost:8000/story/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error("后端请求失败");
      }
      console.log("文本成功发送到后端");

      const data = await response.json();
      console.log("后端返回的数据:", data);

      setResponseText(data.story); // 设置故事文本
      setResponseImage(data.image_url); // 设置图片
      setResponseAudio(data.audio_url); // 设置音频
      setVocabularyWords([data.word1, data.word2, data.word3]); // 提取单词

    } catch (error) {
      console.error("请求失败:", error);
    }
  };

  return (
    <div className="fullPageBackground" style={{ backgroundImage: `url(${fullBackground})` }}>
      <div className="background" style={{ backgroundImage: `url(${background})` }}>
        {/* 显示故事图片 */}
        {responseImage && <img src={responseImage} alt="Story Image" className="story-image" />}

        {/* 显示故事文本 */}
        {responseText && <p className="story-text">{responseText}</p>}

        {/* 显示单词 */}
        {vocabularyWords.length > 0 && (
          <div className="vocabulary-container">
            {vocabularyWords.map((word, index) => (
              <span key={index} className="vocabulary-word">{word}</span>
            ))}
          </div>
        )}

        {/* 语音识别按钮 */}
        <img
          src={isListening ? listeningButton : speakButton}
          alt="speak"
          className="speakButton"
          onClick={startListening}
        />
      </div>
    </div>
  );
}

export default ChatPage;