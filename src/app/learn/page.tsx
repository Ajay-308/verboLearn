"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Navbar from "../home/Navbar";
import { Button } from "@/components/ui/button";
import { Bot } from "lucide-react";
import { Input } from "@/components/ui/input";
interface ChatMessage {
  userMessage: string;
  botMessage: string;
}
const Learn: React.FC = () => {
  const [inputMessage, setInputMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const msgBoxRef = useRef<HTMLDivElement>(null);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch("/api/len", { method: "GET" });
      if (!response.ok) throw new Error("Failed to fetch chat history");

      const data = await response.json();
      setChatHistory(data.reverse()); // data ko ulta kardo taaki latest message sabse upar aaye or chat section mai niche aaye
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };
  // render on page load bencho
  useEffect(() => {
    fetchChatHistory();
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      const response = await axios.post(
        "http://localhost:5000/role",
        { message: inputMessage },
        { withCredentials: true },
      );

      const newMessage = {
        userMessage: inputMessage,
        botMessage: response.data.message,
      };

      console.log("Sending newMessage:", newMessage);

      const re = await fetch("/api/len", {
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
          English Learning
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
                {msg.userMessage && (
                  <div className="mb-1 flex justify-start md:mb-2">
                    <div className="max-w-[80%] rounded-lg bg-blue-600 px-2 py-1 text-white md:px-4 md:py-2">
                      <p className="text-sm font-semibold md:text-base">You</p>
                      <p className="text-sm md:text-base">{msg.userMessage}</p>
                    </div>
                  </div>
                )}
                {msg.botMessage && (
                  <div className="flex justify-end">
                    <div className="max-w-[80%] rounded-lg bg-purple-600 px-2 py-1 text-white md:px-4 md:py-2">
                      <p className="flex items-center text-sm font-semibold md:text-base">
                        <Bot className="mr-1 md:mr-2" size={14} /> Lexi
                      </p>
                      <p className="text-sm md:text-base">{msg.botMessage}</p>
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
};

export default Learn;
