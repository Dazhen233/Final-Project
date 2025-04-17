import React, { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { MusicContext } from './MusicContext'; 
import './App.css';
import background from './assets/startPageBackground.jpg';
import startButton from './assets/startButton.png';
import startPageTitle from './assets/startPageTitle.png';
import backgroundMusic from './assets/backgroundMusic.mp3';
import fullBackground from './assets/fullBackground.jpg';
import nextButton from './assets/nextButton.png'; // 下一步按钮图片


function App() {
  const { playMusic } = useContext(MusicContext);
  const [startAnime, setStartAnime] = useState(false);
  const [hideButton, setHideButton] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);
  const [showNextButton, setShowNextButton] = useState(false);
  const [isClicked, setIsClicked] = useState(false);
  const timeoutIds = useRef([]);
  const musicRef = useRef(new Audio(backgroundMusic));
  const navigate = useNavigate(); // 用于跳转页面

  const handleStart = () => {
    if (hasStarted) return; 
    setHasStarted(true); 
    const audio = new Audio('/clickSound.mp3'); // 点击播放音效（可选）
    audio.play();
    
    setHideButton(true); // 开始执行按钮淡出动画
    
    setTimeout(() => {
      setStartAnime(true); // 按钮完全消失后，角色开始飞入
    }, 1000); // 1秒后隐藏按钮并执行动画
  };
  const playSound = () => {
    const audio = new Audio('/entrance.mp3');
    audio.play().catch(err => console.log('音效播放失败:', err));
  };
  const readTitle = () => {
    const audio = new Audio('/readTitle.mp3');
    audio.play().catch(err => console.log('音效播放失败:', err));
  };

  //**监听全局点击事件**
  useEffect(() => {
    document.addEventListener('click', handleStart);
    return () => {
        document.removeEventListener('click', handleStart); // **防止多次绑定**
    };
  }, [hasStarted]);

  useEffect(() => {
    if (startAnime) {
      // 复制 `timeoutIds.current` 的值，防止 React 清理时值已经被改变
      const timeouts = [
        setTimeout(playSound, 2000),
        setTimeout(playSound, 3000),
        setTimeout(playSound, 3500),
        setTimeout(playSound, 4000),
        setTimeout(readTitle, 5500),
        setTimeout(playMusic, 6500),
        setTimeout(() => setShowNextButton(true), 8000),
      ]
      return () => {
        timeouts.forEach(id => clearTimeout(id)); // 确保清理
      };
    }
  }, [startAnime]); // 监听 `startAnime`

  const handleNextPage = () => {
    setIsClicked(true);  // 按下按钮后修改状态
    setTimeout(() => {
      setIsClicked(false);
    }, 150);
    setTimeout(() => {
      navigate('/style-choose'); // 1秒后跳转
    }, 300);
  };

  return (
    <div className="fullPageBackground" style={{ backgroundImage: `url(${fullBackground})` }}>
      <div className="background" style={{ backgroundImage: `url(${background})` }}>
        {!startAnime && (
          <img
          src={startButton}
          alt="start"
          className={`startButton ${hideButton ? "fade-out" : ""}`}

          />
        )}
        {startAnime && (
          <>
            <img src="/prince.png" alt="prince" className="prince" />
            <img src="/princess.png" alt="princess" className="princess" />
            <img src="/fairy.png" alt="fairy" className="fairy" />
            <img src="/witch.png" alt="witch" className="witch" />
            <img src={startPageTitle} alt="title" className={`startPageTitle ${startAnime ? "delayed-fade-in" : ""}`} />

            {showNextButton&& (
            <img src={nextButton} alt="Next" className={`nextButton fade-in ${isClicked ? "clicked" : ""}`} onClick={handleNextPage} /> // 点击后跳转
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
