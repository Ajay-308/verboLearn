"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Navbar from "../home/Navbar";
import { Button } from "@/components/ui/button";
import { BotIcon } from "lucide-react";
import { Input } from "@/components/ui/input";
import { HiSpeakerWave, HiMiniSpeakerXMark } from "react-icons/hi2";
import { MicIcon } from "lucide-react";
import { userAgent } from "next/server";
interface ChatMessage {
  userMessage: string;
  botMessage: string;
}
const Learn: React.FC = () => {
  const [inputMessage, setInputMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const msgBoxRef = useRef<HTMLDivElement>(null);

  // Fetch chat history from Prisma database
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        console.log("fetching chat hitory");
        const response = await fetch("http://localhost:3000/api/his", {
          method: "GET",
        });
        if (!response.ok) {
          throw new Error("bhai galti ho gyui hai ");
        }
        const data = await response.json();
        setChatHistory(data);
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    };

    fetchChatHistory();
  }, []);

  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    try {
      const response = await axios.post(
        "http://localhost:5000/role",
        { message: inputMessage },
        { withCredentials: true },
      );

      const newMessage: ChatMessage = {
        userMessage: inputMessage,
        botMessage: response.data.message,
      };

      setChatHistory((prevHistory) => [...prevHistory, newMessage]);

      console.log("newMessage", newMessage);
      const re = await fetch("/api/his", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newMessage),
      });

      const data = await response.data;
      console.log(data);

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
    <div className="bg-black">
      <Navbar />
      <div className="bg-gradient text-dark flex min-h-screen flex-col place-content-center  items-center justify-center bg-black ">
        <h1 className="text-warning -mt-24 mb-2 ml-2 mr-auto font-fantasy text-xl font-bold">
          learn english with AI
        </h1>
        <div
          className="bg-light mb-4 h-[33rem] w-[70rem] overflow-y-scroll rounded border p-3"
          ref={msgBoxRef}
        >
          {chatHistory.map((msg, index) => (
            <div key={index} className={`row justify-content-start pl-5`}>
              <div
                className="d-flex flex-column ml-auto rounded border bg-white p-2 text-black shadow"
                style={{
                  width: "fit-content",
                  minWidth: "8rem",
                  maxWidth: "30rem",
                }}
              >
                <div>
                  <strong className="m-1">user</strong>
                </div>
                <h4 className="m-1">{msg.userMessage}</h4>
              </div>

              <div className="row justify-content-end pl-5">
                <div
                  className="d-flex flex-column bg-info w-rounded my-4 -ml-8 mr-auto border p-2 shadow"
                  style={{
                    width: "fit-content",
                    minWidth: "20rem",
                    maxWidth: "55rem",
                  }}
                >
                  <div className="text-white">
                    <BotIcon className="m-1 text-white" size={20} />
                    <strong className="m-1">Jarwis</strong>
                  </div>
                  <h4 className="m-1 text-white">{msg.botMessage}</h4>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="form-group border-5 flex w-[35rem]">
          <Input
            type="text"
            className="form-control  flex-grow  bg-gray-800 text-white"
            name="message"
            onKeyDown={handleKeyDown}
            placeholder="Type your message"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <Button
            className="ml-4 bg-white text-black  hover:scale-110 hover:bg-white"
            onClick={handleSendMessage}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Learn;
