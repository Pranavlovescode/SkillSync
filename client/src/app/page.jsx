"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { TwitterIcon, Loader2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import toast from "react-hot-toast";

export default function Home() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    setIsLoading(true);
    e.preventDefault();
    console.log("the formdata is", formData);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/login/`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = response.data;
      if (response.status == 200) {
        console.log("data", data);
        toast.success(data.message);
      } else {
        toast.error(data.message);
      }
    } catch (error) {
      console.log("error", error);
      toast.error("An error occured while trying to login");
      setIsLoading(false);
      setFormData({
        email: "",
        password: "",
      });
    }
  };

  return (
    <div className="min-h-screen w-full flex">
      <div
        className="hidden lg:flex w-1/2 bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 p-12 
      relative"
      >
        <div className="absolute inset-0 bg-[url('/tweet-bg.jpg')] opacity-20 bg-cover bg-center" />
        <div className="relative z-10 flex flex-col justify-center">
          <TwitterIcon className="h-20 w-20 text-white mb-8" />
          <h1 className="text-5xl font-bold text-white mb-6">
            Join the conversation
          </h1>
          <p className="text-xl text-white/90 max-w-md">
            Connect with friends, share your thoughts, and stay updated with
            what's happening in the world.
          </p>
        </div>
      </div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50">
        <form onSubmit={handleSubmit} className="w-full max-w-md">
          <Card className="w-full max-w-md bg-white shadow-xl">
            <CardHeader className="space-y-1 flex items-center text-center">
              <div className="lg:hidden w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mb-2">
                <TwitterIcon className="h-6 w-6 text-white" />
              </div>
              <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
              <CardDescription>
                Sign in to your account to continue
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="john@example.com"
                  className="h-12"
                  name="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  className="h-12"
                  name="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                />
              </div>
              <div className="text-right">
                <Link
                  href={"/forget-password"}
                  className="text-sm text-blue-500 hover:underline"
                >
                  Forgot password?
                </Link>
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button
                type="submit"
                className="w-full h-12 text-lg bg-blue-500 hover:bg-blue-600"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Loggin In...
                  </>
                ) : (
                  "Login"
                )}
              </Button>
              <div className="text-sm text-center text-gray-600">
                Don't have an account?{" "}
                <Link
                  href={"/signup"}
                  className="text-blue-500 hover:underline"
                >
                  Sign up
                </Link>
              </div>
            </CardFooter>
          </Card>
        </form>
      </div>
    </div>
  );
}
