import React, { useState, useEffect, useRef, useContext} from 'react';
import { useNavigate } from "react-router-dom";
import { MusicContext } from './MusicContext';
import './SecondPage.css';
import background from './assets/startPageBackground.jpg';
import fullBackground from './assets/fullBackground.jpg';
import PawPatrol from './assets/PawPatrol.png';
import SnowWhite from './assets/SnowWhite.png';
import Thomas from './assets/Thomas.png';
import Cinderella from './assets/Cinderella.png';
import backgroundMusic from './assets/backgroundMusic2.mp3';
import voiceHint from './assets/voiceHint.mp3';


function SecondPage() {
  const [showOptions, setShowOptions] = useState([false, false, false, false]);
  const { stopMusic } = useContext(MusicContext);
  const navigate = useNavigate();
  const [isClicked, setIsClicked] = useState(false);
  const [audio] = useState(new Audio(backgroundMusic));
  const [voice] = useState(new Audio(voiceHint));
  

  useEffect(() => {
    stopMusic(); // 进入 SecondPage 时自动停止音乐
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => {
      audio.loop = true; // 设置循环播放
      audio.volume = 0.3; // 设置音量降低 (范围 0.0 - 1.0)
      audio.play().catch((error) => console.log("音乐播放失败，可能是浏览器限制:", error));
    }, 1000); // 等待 1 秒后播放
    return () => {
      clearTimeout(timeout);
      audio.pause();
      audio.currentTime = 0;
    };
  }, []);

  useEffect(() => {
    const voiceTimeout = setTimeout(() => {
      voice.volume = 0.6; // 设置音量
      voice.play().catch(err => console.log("语音播放失败:", err));
    }, 2000);
    return () => clearTimeout(voiceTimeout);
  }, []);

  useEffect(() => {
    setTimeout(() => setShowOptions([true, false, false, false]), 8000);
    setTimeout(() => setShowOptions([true, true, false, false]), 10600);
    setTimeout(() => setShowOptions([true, true, true, false]), 13000);
    setTimeout(() => setShowOptions([true, true, true, true]), 15800);
  }, []);

  const hasNavigated = useRef(false);

  const handleNextPage = (text) => {
      if (hasNavigated.current) return;  // 避免多次跳转
      hasNavigated.current = true;

      setIsClicked(true);
      setTimeout(() => {
          setIsClicked(false);
      }, 150);

      console.log("即将跳转到 ChatPage，传递的数据:", text);

      let volume = audio.volume;
      const fadeOutInterval = setInterval(() => {
          if (volume > 0.05) {
              volume -= 0.05;
              audio.volume = Math.max(volume, 0);
          } else {
              audio.pause();
              audio.currentTime = 0;
              clearInterval(fadeOutInterval);

              // 音量降低完后再跳转
              navigate('/chat', { state: { user_input: text } });
          }
      }, 100);
  };

  return (
    <div className="fullPageBackground" style={{ backgroundImage: `url(${fullBackground})` }}>
      <div className="background" style={{ backgroundImage: `url(${background})` }}>
      {showOptions[0] && (
          <img 
            src={PawPatrol} 
            alt="Option 1" 
            className={`option-img pawPatrol ${showOptions[0] ? "show" : ""}`} 
            onClick={() => handleNextPage("Paw Patrol")}
          />
        )}
        {showOptions[1] && (
          <img 
            src={SnowWhite} 
            alt="Option 2" 
            className={`option-img snowWhite ${showOptions[1] ? "show" : ""}`} 
            onClick={() => handleNextPage("Snow White")}
          />
        )}
        {showOptions[2] && (
          <img 
            src={Thomas} 
            alt="Option 3" 
            className={`option-img thomas ${showOptions[2] ? "show" : ""}`} 
            onClick={() => handleNextPage("Thomas")}
          />
        )}
        {showOptions[3] && (
          <img 
            src={Cinderella} 
            alt="Option 4" 
            className={`option-img cinderella ${showOptions[3] ? "show" : ""}`} 
            onClick={() => handleNextPage("Cinderella")}
          />
        )}
      </div>
    </div>
  );
}
export default SecondPage;