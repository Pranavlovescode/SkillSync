import { NextRequest, NextResponse } from "next/server";

export function middleware(req) {
  const sessionCookie = req.cookies.get("sessionId");
  const session = sessionCookie ? sessionCookie.value : null;
  const path = req.nextUrl.pathname;

  const publicPaths =
    path === "/" || path === "/signup" || path.startsWith("/api/auth");

  // If user is logged in and trying to access login/signup pages,
  // redirect to skills page
  if (publicPaths && session) {
    console.log("user logged in, redirecting...");
    return NextResponse.redirect(new URL("/skills", req.url));
  }

  // If user is not logged in and trying to access protected pages,
  // redirect to login page
  if (!publicPaths && !session) {
    const url = new URL("/", req.url);
    console.log("user not logged in, redirecting...");
    return NextResponse.redirect(url);
  }

  // Continue with request
  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/signup", "/skills/:path*",'/skills'],
};
