"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { UserButton } from "@clerk/nextjs";
import Link from "next/link";
import { BellIcon, Menu, X } from "lucide-react";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="fixed top-0 z-50 w-full border-b border-purple-500/20 bg-black/50 backdrop-blur-xl">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <div className="flex items-center gap-2">
          <div className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-2xl font-bold text-transparent">
            <Link href="/home">VerboLearn</Link>
          </div>
        </div>

        {/* Mobile menu button */}
        <button
          className="text-gray-300 focus:outline-none md:hidden"
          onClick={toggleMenu}
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        {/* Desktop menu */}
        <div className="hidden items-center gap-8 md:flex">
          <Link
            href="/home#features"
            className="text-gray-300 transition hover:text-purple-400"
          >
            Features
          </Link>
          <a
            href="#about"
            className="text-gray-300 transition hover:text-purple-400"
          >
            About
          </a>
          <a
            href="/contact"
            className="text-gray-300 transition hover:text-purple-400"
          >
            Contact
          </a>
          <Link href="/tasks">
            <BellIcon className="cursor-pointer text-gray-300">
              <title>Notification</title>
            </BellIcon>
          </Link>
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
          <Button className="space-x-20 bg-purple-600 text-white hover:bg-purple-700 md:mr-0 lg:-mr-4 xl:-mr-44">
            Get Started
          </Button>
        </div>
      </div>

      {isMenuOpen && (
        <div className="bg-black/90 py-4 md:hidden">
          <div className="container mx-auto flex flex-col gap-4 px-4">
            <Link
              href="/home#features"
              className="text-gray-300 transition hover:text-purple-400"
              onClick={toggleMenu}
            >
              Features
            </Link>
            <a
              href="#about"
              className="text-gray-300 transition hover:text-purple-400"
              onClick={toggleMenu}
            >
              About
            </a>
            <a
              href="/contact"
              className="text-gray-300 transition hover:text-purple-400"
              onClick={toggleMenu}
            >
              Contact
            </a>
            <div className="flex items-center justify-between">
              <Link href={""} onClick={toggleMenu}>
                <BellIcon className="cursor-pointer text-gray-300">
                  <title>Notification</title>
                </BellIcon>
              </Link>
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
            </div>
            <Button className="w-full bg-purple-600 text-white hover:bg-purple-700">
              Get Started
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
