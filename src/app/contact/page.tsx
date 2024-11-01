import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import Navbar from "../home/Navbar";
import Footer from "../home/footer";

export default function Component() {
  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-black px-4 py-12 text-white">
        <div className="mx-auto mt-24 max-w-2xl space-y-8">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Contact Us
            </h1>
            <p className="text-gray-400 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              We&apos;d love to hear from you. Please fill out this form.
            </p>
          </div>

          <Card className="border-0 bg-gradient-to-br from-purple-900/50 to-blue-900/50 shadow-xl">
            <CardContent className="p-6">
              <form className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="name" className="text-white">
                    Name
                  </Label>
                  <Input
                    id="name"
                    placeholder="John Doe"
                    className="border-white/10 bg-white/5 text-white placeholder:text-gray-400"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone" className="text-white">
                    Phone Number
                  </Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+1234567890"
                    className="border-white/10 bg-white/5 text-white placeholder:text-gray-400"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="address" className="text-white">
                    Address
                  </Label>
                  <Input
                    id="address"
                    placeholder="123 Main St, City, Country"
                    className="border-white/10 bg-white/5 text-white placeholder:text-gray-400"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="query" className="text-white">
                    Your Query
                  </Label>
                  <Textarea
                    id="query"
                    placeholder="Please describe how we can help you..."
                    className="min-h-[150px] border-white/10 bg-white/5 text-white placeholder:text-gray-400"
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full rounded-md bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-2 font-medium text-white transition-colors hover:from-purple-700 hover:to-blue-700"
                >
                  Submit
                </Button>
              </form>
            </CardContent>
          </Card>

          <p className="text-center text-gray-400">
            We&apos;ll get back to you within 24 hours.
          </p>
        </div>
      </div>
      <div className="-mt-24">
        <Footer />
      </div>
    </>
  );
}
