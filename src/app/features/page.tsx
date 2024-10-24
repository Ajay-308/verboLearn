import React from "react";
import { Bot, Brain, MessageSquare } from "lucide-react";
import Link from "next/link";

const page = () => {
  return (
    <section id="features" className="relative py-20">
      <div className="container mx-auto px-4">
        <div className="grid gap-8 md:grid-cols-3">
          {[
            {
              icon: <Bot className="h-10 w-10 text-purple-400" />,
              title: "AI Interview Practice",
              link: "/interview",
              description:
                "Practice with our intelligent AI interviewer and receive instant feedback",
            },
            {
              icon: <Brain className="h-10 w-10 text-blue-400" />,
              title: "Smart Resume Analysis",
              link: "/resume",
              description:
                "Get personalized recommendations to improve your resume",
            },
            {
              icon: <MessageSquare className="h-10 w-10 text-purple-400" />,
              title: "English Mastery",
              link: "/learn",
              description:
                "Enhance your language skills through AI-powered conversations",
            },
          ].map((feature, index) => (
            <div key={index} className="group relative">
              <Link href={feature.link}>
                <div className="relative rounded-xl border border-purple-500/20 p-8 backdrop-blur-sm">
                  <div className="mb-4">{feature.icon}</div>
                  <h3 className="mb-3 text-xl font-semibold text-white">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400">{feature.description}</p>
                  <div className="absolute inset-0 transform rounded-xl bg-gradient-to-r from-purple-600/10 to-blue-600/10 transition-transform duration-300 group-hover:scale-105" />
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default page;
