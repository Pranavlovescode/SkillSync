"use client";

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';


export default function SkillsLayout({ children }) {
  const pathname = usePathname();
  
  const navItems = [
    { name: 'All Skills', path: '/skills' },
    { name: 'My Skills', path: '/skills/my-skills' },
    { name: 'Trending', path: '/skills/trending' },
    { name: 'Recommendations', path: '/skills/recommendations' },
  ];
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Skills Navigation */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="container flex justify-between items-center mx-auto px-4 max-w-6xl">
          <nav className="flex overflow-x-auto py-4 no-scrollbar">
            {navItems.map((item) => {
              const isActive = pathname === item.path;
              return (
                <Link
                  key={item.path}
                  href={item.path}
                  className={`whitespace-nowrap px-5 py-2 rounded-full text-sm font-medium mr-2 transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {item.name}
                </Link>
              );
            })}
            
          </nav>
          <Image src={'https://res.cloudinary.com/dwsjntvgq/image/upload/v1743408181/SkillSync/profile_photo/s4qbhsl5b1uqshpmyua1.jpg'} width={40} height={10} alt='user' className='rounded-full'/>
        </div>
      </div>
      
      {/* Main Content */}
      <main>{children}</main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 mt-20">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-gray-600 text-sm">
                © {new Date().getFullYear()} SkillSync. All rights reserved.
              </p>
            </div>
            <div className="flex space-x-4">
              <Link href="/about" className="text-gray-600 hover:text-blue-600 text-sm">
                About
              </Link>
              <Link href="/privacy" className="text-gray-600 hover:text-blue-600 text-sm">
                Privacy
              </Link>
              <Link href="/terms" className="text-gray-600 hover:text-blue-600 text-sm">
                Terms
              </Link>
              <Link href="/contact" className="text-gray-600 hover:text-blue-600 text-sm">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
} 