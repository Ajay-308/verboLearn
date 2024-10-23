import React from "react";
import logo from "@/assets/logo.png";
import { Button } from "@/components/ui/button";
import { UserButton } from "@clerk/nextjs";
import Image from "next/image";
import Link from "next/link";
import lo from "@/assets/lo-removebg-preview.png";

const Navbar: React.FC = () => {
  return (
    <>
      <nav className="fixed top-0 z-50 w-full border-b border-purple-500/20 bg-black/50 backdrop-blur-xl">
        <div className="container mx-auto flex items-center justify-between px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-2xl font-bold text-transparent">
              VerboLearn
            </div>
          </div>

          <div className="hidden items-center gap-8 md:flex">
            <a
              href="#features"
              className="text-gray-300 transition hover:text-purple-400"
            >
              Features
            </a>
            <a
              href="#about"
              className="text-gray-300 transition hover:text-purple-400"
            >
              About
            </a>
            <a
              href="#contact"
              className="text-gray-300 transition hover:text-purple-400"
            >
              Contact
            </a>
            <UserButton
              afterSignOutUrl="/"
              appearance={{
                elements: {
                  avatarBox: {
                    width: "2.7rem",
                    height: "2.7rem",
                  },
                },
              }}
            />
            <Button className="bg-purple-600 text-white hover:bg-purple-700">
              Get Started
            </Button>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
