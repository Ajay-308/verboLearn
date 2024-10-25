"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot } from "lucide-react";
import Navbar from "@/app/home/Navbar";

interface ChatMessage {
  user: string;
  jarwis: string;
}

export default function InterviewPrepComponent() {
  const [inputMessage, setInputMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>(() => {
    const storedChatHistory = localStorage.getItem("chatHistory");
    return storedChatHistory ? JSON.parse(storedChatHistory) : [];
  });
  const msgBoxRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      const response = await axios.post(
        "http://localhost:5000/chat",
        { message: inputMessage },
        { withCredentials: true },
      );

      const newMessage: ChatMessage = {
        user: inputMessage,
        jarwis: response.data.message,
      };

      setChatHistory((prevHistory) => [...prevHistory, newMessage]);
      localStorage.setItem(
        "chatHistory",
        JSON.stringify([...chatHistory, newMessage]),
      );
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

  return (
    <>
      <Navbar />
      <div className="flex h-screen flex-col bg-gray-950 text-gray-100">
        <h1 className="mt-20 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text py-2 text-center text-2xl font-bold text-transparent md:py-4 md:text-3xl">
          AI Interview Prep
        </h1>

        <div className="flex flex-grow flex-col overflow-hidden p-2 md:p-4">
          <h2 className="-mt-4 mb-2 text-lg text-blue-400 md:text-xl">
            Practice Session
          </h2>
          <div
            className="mb-2 flex-grow overflow-y-auto rounded-lg border border-gray-800 p-2 md:p-4"
            ref={msgBoxRef}
          >
            {chatHistory.map((msg, index) => (
              <div key={index} className="mb-2 md:mb-4">
                {msg.user && (
                  <div className="mb-1 flex justify-start md:mb-2">
                    <div className="max-w-[80%] rounded-lg bg-blue-600 px-2 py-1 text-white md:px-4 md:py-2">
                      <p className="text-sm font-semibold md:text-base">You</p>
                      <p className="text-sm md:text-base">{msg.user}</p>
                    </div>
                  </div>
                )}
                {msg.jarwis && (
                  <div className="flex justify-end">
                    <div className="max-w-[80%] rounded-lg bg-purple-600 px-2 py-1 text-white md:px-4 md:py-2">
                      <p className="flex items-center text-sm font-semibold md:text-base">
                        <Bot className="mr-1 md:mr-2" size={14} /> AI
                        Interviewer
                      </p>
                      <p className="text-sm md:text-base">{msg.jarwis}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Type your response..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-grow border-gray-700 bg-gray-800 text-sm text-white md:text-base"
            />
            <Button
              onClick={handleSendMessage}
              className="bg-blue-600 text-sm hover:bg-blue-700 md:text-base"
            >
              Send
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
