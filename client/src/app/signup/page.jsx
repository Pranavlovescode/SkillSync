"use client";
import React, { useState } from "react";
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
import { TwitterIcon, Loader2 } from "lucide-react";
import toast from "react-hot-toast";
import axios from "axios";
import Link from "next/link";

export default function Signup() {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handelSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    console.log("Form Data", formData);
    try {
      if (formData.password == formData.confirmPassword) {
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/signup/`,
          {
            first_name: formData.first_name,
            last_name: formData.last_name,
            username: formData.username,
            email: formData.email,
            password: formData.password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (response.status == 201) {
          console.log("data", response.data);
          toast.success(response.data.message);
          setFormData({
            first_name: "",
            last_name: "",
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
          })
          setIsLoading(false);
        }
      } else {
        toast.error("Passwords do not match");
        setIsLoading(false);
      }
    } catch (error) {
      console.error("Error", error);
      toast.error("An error occured while trying to create an account");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex">
      {/* Left Section - Hero/Branding */}
      <div className="hidden lg:flex w-1/2 bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 p-12 relative">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1579548122080-c35fd6820ecb')] opacity-20 bg-cover bg-center" />
        <div className="relative z-10 flex flex-col justify-center">
          <TwitterIcon className="h-20 w-20 text-white mb-8" />
          <h1 className="text-5xl font-bold text-white mb-6">
            Join SkillSync today
          </h1>
          <p className="text-xl text-white/90 max-w-md">
            Share your thoughts, follow your interests, and be part of the
            global conversation.
          </p>
        </div>
      </div>

      {/* Right Section - Signup Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50">
        <form onSubmit={handelSubmit} className="w-full max-w-md">
          <Card className="w-full max-w-md bg-white shadow-xl">
            <CardHeader className="space-y-1 flex items-center text-center">
              <div className="lg:hidden w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mb-2">
                <TwitterIcon className="h-6 w-6 text-white" />
              </div>
              <CardTitle className="text-2xl font-bold">
                Create an account
              </CardTitle>
              <CardDescription>
                Enter your details to get started
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">First Name</Label>
                <Input
                  id="first_name"
                  placeholder="John"
                  name="first_name"
                  className="h-12"
                  value={formData.first_name}
                  onChange={(e) =>
                    setFormData({ ...formData, first_name: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">Last Name</Label>
                <Input
                  id="last_name"
                  placeholder="Doe"
                  name="last_name"
                  className="h-12"
                  value={formData.last_name}
                  onChange={(e) =>
                    setFormData({ ...formData, last_name: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  placeholder="@johndoe"
                  name="username"
                  className="h-12"
                  value={formData.username}
                  onChange={(e) =>
                    setFormData({ ...formData, username: e.target.value })
                  }
                />
              </div>
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
                  name="password"
                  className="h-12"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  className="h-12"
                  value={formData.confirmPassword}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      confirmPassword: e.target.value,
                    })
                  }
                />
              </div>
              <div className="text-sm text-gray-600">
                By signing up, you agree to our{" "}
                <a href="#" className="text-blue-500 hover:underline">
                  Terms
                </a>
                ,{" "}
                <a href="#" className="text-blue-500 hover:underline">
                  Privacy Policy
                </a>
                , and{" "}
                <a href="#" className="text-blue-500 hover:underline">
                  Cookie Use
                </a>
                .
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button
                type="submit"
                className="w-full h-12 text-lg bg-blue-500 hover:bg-blue-600"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating Account...
                  </>
                ) : (
                  "Sign up"
                )}
              </Button>
              <div className="text-sm text-center text-gray-600">
                Already have an account?{" "}
                <Link href={'/'} className="text-blue-500 hover:underline">
                  Sign in
                </Link>
              </div>
            </CardFooter>
          </Card>
        </form>
      </div>
    </div>
  );
}
