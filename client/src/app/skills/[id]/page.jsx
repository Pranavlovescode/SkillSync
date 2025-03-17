"use client";

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { skillsApi } from '@/lib/api';
import { motion } from 'framer-motion';

// Loading component
const SkillDetailLoading = () => (
  <div className="container mx-auto px-4 py-8 max-w-4xl">
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="h-10 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6 mb-6"></div>
        
        <div className="flex gap-2 mb-4">
          <div className="h-8 bg-gray-200 rounded-full w-24"></div>
          <div className="h-8 bg-gray-200 rounded-full w-32"></div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="flex items-center gap-4 mb-4">
            <div className="h-10 w-10 bg-gray-200 rounded-full"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default function SkillDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [skill, setSkill] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchSkillDetail = async () => {
      try {
        setIsLoading(true);
        // In a real app, you would fetch the skill details from the API
        // const data = await skillsApi.getSkillById(params.id);
        
        // For now, we'll use mock data
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API delay
        
        // Mock data for skill detail
        const mockSkill = {
          id: parseInt(params.id),
          name: ["JavaScript", "React", "Python", "UI/UX Design"][params.id % 4],
          level: ["Beginner", "Intermediate", "Advanced", "Expert"][params.id % 4],
          description: "This is a detailed description of the skill. It includes information about experience, projects, and certifications related to this skill.",
          category: {
            id: params.id % 4 + 1,
            name: ["Programming Languages", "Web Development", "Data Science", "Design"][params.id % 4]
          },
          endorsements: 20 + (params.id % 30),
          endorsedBy: [
            { id: 1, name: "John Doe", avatar: "https://randomuser.me/api/portraits/men/1.jpg", title: "Senior Developer" },
            { id: 2, name: "Jane Smith", avatar: "https://randomuser.me/api/portraits/women/2.jpg", title: "Product Manager" },
            { id: 3, name: "Alex Johnson", avatar: "https://randomuser.me/api/portraits/men/3.jpg", title: "UX Designer" }
          ],
          projects: [
            { id: 1, name: "E-commerce Platform", description: "Built a full-stack e-commerce platform" },
            { id: 2, name: "Data Visualization Dashboard", description: "Created interactive data visualizations" }
          ]
        };
        
        setSkill(mockSkill);
      } catch (err) {
        console.error("Error fetching skill details:", err);
        setError("Failed to load skill details. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    if (params.id) {
      fetchSkillDetail();
    }
  }, [params.id]);

  const handleEndorse = async () => {
    try {
      // In a real app, you would call the API to endorse the skill
      // await skillsApi.endorseSkill(skill.id);
      
      // For now, we'll just update the local state
      setSkill(prev => ({
        ...prev,
        endorsements: prev.endorsements + 1,
        endorsedBy: [
          { 
            id: prev.endorsedBy.length + 1, 
            name: "You", 
            avatar: "https://randomuser.me/api/portraits/lego/1.jpg", 
            title: "Your Title" 
          },
          ...prev.endorsedBy
        ]
      }));
    } catch (err) {
      console.error("Error endorsing skill:", err);
    }
  };

  if (isLoading) {
    return <SkillDetailLoading />;
  }

  if (error || !skill) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl text-center">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p>{error || "Skill not found"}</p>
          <button 
            className="mt-2 text-red-600 hover:text-red-800 font-medium"
            onClick={() => router.push('/skills')}
          >
            Back to Skills
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Breadcrumb */}
      <nav className="flex mb-6 text-sm text-gray-500">
        <Link href="/skills" className="hover:text-blue-600">
          Skills
        </Link>
        <span className="mx-2">/</span>
        <Link href={`/skills?category=${skill.category.id}`} className="hover:text-blue-600">
          {skill.category.name}
        </Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{skill.name}</span>
      </nav>

      {/* Skill Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white rounded-lg shadow-md p-6 mb-8"
      >
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{skill.name}</h1>
            <div className="flex items-center gap-2 mb-4">
              <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                {skill.level}
              </span>
              <span className="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                {skill.category.name}
              </span>
            </div>
          </div>
          <div className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
            {skill.endorsements} endorsements
          </div>
        </div>

        <p className="text-gray-700 mb-6">{skill.description}</p>

        <div className="flex gap-3">
          <button
            onClick={handleEndorse}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
            </svg>
            Endorse
          </button>
          <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
            </svg>
            Share
          </button>
        </div>
      </motion.div>

      {/* Endorsements Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-white rounded-lg shadow-md p-6 mb-8"
      >
        <h2 className="text-xl font-bold text-gray-800 mb-4">Endorsed by</h2>
        
        {skill.endorsedBy.length > 0 ? (
          <div className="space-y-4">
            {skill.endorsedBy.map(person => (
              <div key={person.id} className="flex items-center gap-4">
                <img
                  src={person.avatar}
                  alt={person.name}
                  className="w-10 h-10 rounded-full object-cover"
                />
                <div>
                  <h3 className="font-medium text-gray-900">{person.name}</h3>
                  <p className="text-sm text-gray-500">{person.title}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No endorsements yet. Be the first to endorse!</p>
        )}
      </motion.div>

      {/* Projects Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <h2 className="text-xl font-bold text-gray-800 mb-4">Related Projects</h2>
        
        {skill.projects.length > 0 ? (
          <div className="space-y-4">
            {skill.projects.map(project => (
              <div key={project.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
                <h3 className="font-medium text-gray-900 mb-1">{project.name}</h3>
                <p className="text-sm text-gray-600">{project.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No projects associated with this skill yet.</p>
        )}
      </motion.div>
    </div>
  );
} 