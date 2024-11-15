import { auth } from "@clerk/nextjs";
import { Metadata } from "next";

import { Button } from "@/components/ui/button";
import Image from "next/image";

import { prisma } from "@/lib/db";
import { error } from "console";
import bg from "@/assets/bg.png";
import { ArrowRight, Sparkles, Bot, Brain, MessageSquare } from "lucide-react";
import Link from "next/link";
import Footer from "./footer";
export const metadata: Metadata = {
  title: "Talk User",
};
interface EmailAddress {
  email_address: string;
  id: string;
}

interface UserAttributes {
  username: string;
  last_name: string;
  first_name: string;
  updated_at: number;
  email_addresses: EmailAddress[];
}

const Home = async () => {
  const { userId } = auth();
  if (userId) {
    const user = await prisma.user.findUnique({
      where: {
        externalId: userId,
      },
    });
    const userAttribute: UserAttributes =
      user?.attributes as unknown as UserAttributes;
    try {
      if (userAttribute.email_addresses[0].email_address) {
        console.log(userAttribute.email_addresses[0].email_address);
        console.log(userAttribute.username);
      }
    } catch (e) {
      error("user not found");
    }
  }

  const features = [
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
      description: "Get personalized recommendations to improve your resume",
    },
    {
      icon: <MessageSquare className="h-10 w-10 text-purple-400" />,
      title: "English Mastery",
      link: "/learn",
      description:
        "Enhance your language skills through AI-powered conversations",
    },
  ];
  return (
    <div className="min-h-screen overflow-hidden bg-black text-white">
      <div className="relative h-[100vh] overflow-hidden">
        {/* Background Image */}
        <Image
          src={bg}
          alt="Background image"
          layout="fill"
          objectFit="cover"
          priority
        />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-purple-900/40 to-blue-900/40" />

        {/* Animated Circles */}
        <div className="absolute left-1/4 top-20 h-2 w-2 animate-pulse rounded-full bg-purple-400" />
        <div className="absolute right-1/3 top-40 h-3 w-3 animate-pulse rounded-full bg-blue-400" />
        <div className="absolute bottom-20 left-1/3 h-4 w-4 animate-pulse rounded-full bg-purple-500" />

        {/* Main Content (Text Overlay) */}
        <div className="relative z-10 flex h-full items-center justify-center">
          <div className="container mx-auto px-4 text-center">
            <h1 className="mb-6 text-4xl font-bold text-white md:text-6xl">
              Unlock Your Career Growth with{" "}
              <span className="text-gradient bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                <Link href="/home">VerboLearn</Link>
              </span>
            </h1>
            <p className="mx-auto mb-8 max-w-2xl text-lg text-gray-300 md:text-xl">
              Master English, ace interviews, and build the perfect resume with
              our AI-powered platform
            </p>
            <Button className="bg-cyan-500 px-8 py-6 text-lg hover:bg-cyan-600">
              Begin Your Journey <ArrowRight className="ml-2" />
            </Button>
          </div>
        </div>
      </div>

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

      {/* How It Works */}
      <section className="relative py-20">
        <div className="container mx-auto px-4">
          <h2 className="mb-16 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-center text-3xl font-bold text-transparent">
            Your Learning Journey
          </h2>
          <div className="mx-auto flex max-w-5xl flex-col items-center justify-center gap-8 md:flex-row">
            {[
              {
                step: "01",
                title: "Upload",
                desc: "Share your resume or start a conversation",
              },
              {
                step: "02",
                title: "Analyze",
                desc: "Receive AI-powered insights",
              },
              {
                step: "03",
                title: "Improve",
                desc: "Implement feedback and track progress",
              },
            ].map((item, index) => (
              <div key={index} className="group relative w-full md:w-1/3">
                <div className="absolute inset-0 transform rounded-xl bg-gradient-to-b from-purple-600/10 to-blue-600/10 transition-transform duration-300 group-hover:scale-105" />
                <div className="relative p-8 text-center">
                  <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-purple-600 to-blue-600 text-2xl font-bold">
                    {item.step}
                  </div>
                  <h3 className="mb-3 text-xl font-semibold text-white">
                    {item.title}
                  </h3>
                  <p className="text-gray-400">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative overflow-hidden py-20">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-900/20 to-blue-900/20" />
        <div className="container relative mx-auto px-4">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="mb-6 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-4xl font-bold text-transparent">
              Ready to Transform Your Career?
            </h2>
            <p className="mb-8 text-gray-300">
              Join thousands of professionals who have already elevated their
              careers with VerboLearn
            </p>
            <Button className="bg-gradient-to-r from-purple-600 to-blue-600 px-8 py-6 text-white hover:from-purple-700 hover:to-blue-700">
              Get Started Now <Sparkles className="ml-2" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Home;
