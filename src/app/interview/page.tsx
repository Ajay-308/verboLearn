"use client";
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, MicIcon } from "lucide-react";
import Navbar from "@/app/home/Navbar";
import { keyframes } from "@emotion/react";

interface ChatMessage {
  userMessage: string;
  botMessage: string;
}

export default function InterviewPrepComponent() {
  const [inputMessage, setInputMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [voiceData, setVoiceData] = useState("");
  const [error, setError] = useState("");
  const [listening, setListening] = useState(false); // New state for listening overlay

  const msgBoxRef = useRef<HTMLDivElement>(null);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch("/api/his", { method: "GET" });
      if (!response.ok) throw new Error("Failed to fetch chat history");

      const data = await response.json();
      setChatHistory(data.reverse());
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      const response = await axios.post(
        "http://localhost:5000/chat",
        { message: inputMessage },
        { withCredentials: true },
      );

      const newMessage = {
        userMessage: inputMessage,
        botMessage: response.data.message,
      };

      console.log("Sending newMessage:", newMessage);

      const re = await fetch("/api/his", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newMessage),
      });

      const data = await re.json();
      console.log("Response from server:", data);
      fetchChatHistory();

      setInputMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  //for handling listen event
  const handleListenSubmit = async (message: string = inputMessage) => {
    if (!message.trim()) return;

    try {
      const response = await axios.post(
        "http://localhost:5000/chat",
        { message },
        { withCredentials: true },
      );

      const newMessage = {
        userMessage: inputMessage,
        botMessage: response.data.message,
      };

      const re = await fetch("/api/his", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newMessage),
      });

      const data = await re.json();
      fetchChatHistory();
      setInputMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (msgBoxRef.current) {
      msgBoxRef.current.scrollTop = msgBoxRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleListen = async () => {
    try {
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = "en-US";
      setListening(true); // Show overlay

      recognition.start();

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setVoiceData(transcript);
        setInputMessage(transcript);
        recognition.stop();
      };

      recognition.onerror = (event) => {
        setError(`Speech recognition error: ${event.error}`);
        recognition.stop();
      };

      recognition.onend = () => setListening(false); // Hide overlay when recognition stops
    } catch (error) {
      setError(`Error: ${error}`);
      setListening(false);
    }
  };

  const vibrateAnimation = keyframes`
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  `;

  return (
    <>
      <Navbar />
      <div className="flex h-screen flex-col bg-gray-950 text-gray-100">
        <h1 className="mt-12 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text py-4 text-center text-3xl font-bold text-transparent md:mt-20 md:text-4xl">
          AI Interview Prep
        </h1>
        <div className="flex flex-grow flex-col overflow-hidden p-4">
          <h2 className="mb-4 text-xl text-blue-400 md:text-2xl">
            Practice Session
          </h2>
          <div
            className="scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-700 mb-4 flex-grow overflow-y-auto rounded-lg border border-gray-800 p-4"
            ref={msgBoxRef}
          >
            {chatHistory.map((msg, index) => (
              <div key={index} className="mb-6">
                {msg.userMessage && (
                  <div className="mb-3 flex justify-start">
                    <div className="max-w-[80%] rounded-lg bg-blue-600 px-4 py-3 text-white shadow-xl">
                      <p className="text-sm font-semibold md:text-base">You</p>
                      <p className="text-sm md:text-base">{msg.userMessage}</p>
                    </div>
                  </div>
                )}
                {msg.botMessage && (
                  <div className="mt-4 flex justify-end">
                    <div className="max-w-[80%] rounded-lg bg-gray-800 px-4 py-4 text-white shadow-xl">
                      <p className="flex items-center text-sm font-semibold md:text-base">
                        <Bot className="mr-3" size={18} />{" "}
                        <span>AI Interviewer</span>
                      </p>
                      <p className="text-sm leading-relaxed md:text-base">
                        {msg.botMessage}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-4 flex items-center gap-4">
            <Input
              type="text"
              placeholder="Type your response..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-grow rounded-lg border-2 border-gray-700 bg-gray-800 px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 md:text-base"
            />
            <MicIcon
              className="ml-4 h-10  w-16 cursor-pointer rounded bg-blue-600 py-2 text-black"
              size={25}
              onClick={() => handleListen()}
            />
            <Button
              onClick={handleSendMessage}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm text-white transition-all duration-300 hover:bg-blue-700 md:text-base"
            >
              <Send size={20} />
            </Button>
          </div>
        </div>
      </div>
      {listening && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <MicIcon
            className="text-blue-600"
            size={100}
            style={{
              animation: `${vibrateAnimation} 0.5s ease-in-out infinite`,
            }}
          />
        </div>
      )}
    </>
  );
}
