import React from "react";
import { Instagram, GithubIcon, LinkedinIcon, MailIcon } from "lucide-react";
import logo from "@/assets/footor logo.png";
import Image from "next/image";

const Footer: React.FC = () => {
  return (
    <div className="bg-black p-4 text-white">
      <div className=" flex items-center justify-center gap-8">
        <a
          href="YOUR_INSTAGRAM_URL"
          target="_blank"
          rel="noopener noreferrer"
          className="cursor-pointer hover:text-pink-600"
        >
          <Instagram size={24} />
        </a>
        <a
          href="https://github.com/Ajay-308/TALK_user"
          target="_blank"
          rel="noopener noreferrer"
          className="cursor-pointer hover:text-white"
        >
          <GithubIcon size={24} />
        </a>
        <a
          href="YOUR_LINKEDIN_URL"
          target="_blank"
          rel="noopener noreferrer"
          className="cursor-pointer hover:text-blue-500"
        >
          <LinkedinIcon size={24} />
        </a>
        <a
          href="mailto:mr.ajaykumar308@gmail.com"
          className="cursor-pointer hover:text-red-500    "
        >
          <MailIcon size={24} />
        </a>
      </div>
      <div className="mt-4 text-center">
        <Image
          src={logo}
          alt="bam bhole"
          className="mb-8 ml-[48rem] mt-8 h-10 w-10 content-center text-center"
        />
        © 2024 Bam Bhole. All rights reserved.
      </div>
    </div>
  );
};

export default Footer;
