import { Button } from "@/components/ui/button";
import { auth } from "@clerk/nextjs";
import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { redirect } from "next/navigation";
import Navbar from "./home/Navbar";
import Image from "next/image";
import bg from "@/assets/bg.png";

const Home: React.FC = () => {
  const { userId } = auth();

  if (userId) redirect("/home");

  return (
    <div>
      <Navbar />
      <section className="min-h-screen overflow-hidden bg-black text-white">
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
                Master English, ace interviews, and build the perfect resume
                with our AI-powered platform
              </p>
              <Button className="bg-cyan-500 px-8 py-6 text-lg hover:bg-cyan-600">
                <Link className="mr-8 flex items-center" href="/home">
                  Begin Your Journey <ArrowRight className="ml-2" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
