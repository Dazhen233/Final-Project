import { createContext, useState, useEffect, useRef } from 'react';
import backgroundMusic from './assets/backgroundMusic.mp3';

export const MusicContext = createContext(); // 确保正确创建 context

export function MusicProvider({ children }) {
  const musicRef = useRef(new Audio(backgroundMusic));
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    musicRef.current.loop = true;
    musicRef.current.volume = 0.5;
    
    return () => {
      musicRef.current.pause();
      musicRef.current.currentTime = 0;
      setIsPlaying(false);
    };
  }, []);

  const playMusic = () => {
    if (!isPlaying) {
      musicRef.current.play().then(() => setIsPlaying(true)).catch(err => console.log("音乐播放失败:", err));
    }
  };

  const stopMusic = () => {
    console.log("stopMusic 被调用！"); // 添加日志，调试是否被调用
    musicRef.current.pause();
    musicRef.current.currentTime = 0;
    setIsPlaying(false);
  };

  return (
    <MusicContext.Provider value={{ playMusic, stopMusic }}> {/* 确保 stopMusic 在这里 */}
      {children}
    </MusicContext.Provider>
  );
}
