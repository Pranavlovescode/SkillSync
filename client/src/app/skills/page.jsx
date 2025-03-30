"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { skillSyncApi } from '@/lib/api';
import { Suspense } from 'react';

// Fallback loading component
const SkillsLoading = () => (
  <div className="container mx-auto px-4 py-8 max-w-6xl">
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
      
      <div className="bg-gray-100 rounded-lg p-4 mb-8">
        <div className="h-10 bg-gray-200 rounded mb-4"></div>
        <div className="flex gap-2">
          <div className="h-8 bg-gray-200 rounded-full w-24"></div>
          <div className="h-8 bg-gray-200 rounded-full w-32"></div>
          <div className="h-8 bg-gray-200 rounded-full w-28"></div>
        </div>
      </div>
      
      {[1, 2, 3].map(i => (
        <div key={i} className="mb-8">
          <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map(j => (
              <div key={j} className="bg-gray-100 rounded-lg p-4 h-32"></div>
            ))}
          </div>
        </div>
      ))}
    </div>
  </div>
);

// Skill Card Component
const SkillCard = ({ skill, onEndorse }) => {
  return (
    <motion.div 
      className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-all"
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold text-lg text-gray-800">{skill.name}</h3>
          <p className="text-sm text-gray-500">{skill.level}</p>
        </div>
        <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
          {skill.endorsements} endorsements
        </div>
      </div>
      <div className="mt-3 flex justify-between">
        <button 
          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          onClick={() => onEndorse(skill.id)}
        >
          Endorse
        </button>
        <Link href={`/skills/${skill.id}`} className="text-sm text-gray-600 hover:text-gray-800">
          Details
        </Link>
      </div>
    </motion.div>
  );
};

// Category Section Component
const CategorySection = ({ category, isExpanded, toggleExpand, onEndorse }) => {
  // Check if category has skills before rendering
  const hasSkills = Array.isArray(category.skills) && category.skills.length > 0;
  
  return (
    <div className="mb-8">
      <div 
        className="flex justify-between items-center cursor-pointer mb-4"
        onClick={() => toggleExpand(category.id)}
      >
        <h2 className="text-xl font-bold text-gray-800">{category.name}</h2>
        {hasSkills && (
          <button className="text-blue-600 hover:text-blue-800">
            {isExpanded ? "Show Less" : "Show All"}
          </button>
        )}
      </div>
      
      {hasSkills ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {category.skills.slice(0, isExpanded ? category.skills.length : 3).map(skill => (
            <SkillCard 
              key={skill.id} 
              skill={skill} 
              onEndorse={onEndorse}
            />
          ))}
        </div>
      ) : (
        <div className="bg-gray-50 rounded-lg p-6 text-center">
          <p className="text-gray-500">No skills found in this category.</p>
          <Link href="/skills/add" className="mt-2 inline-block text-blue-600 hover:text-blue-800">
            Add a skill
          </Link>
        </div>
      )}
    </div>
  );
};

// Main Skills Page Component
function SkillsContent() {
  const [categories, setCategories] = useState([]);
  const [expandedCategories, setExpandedCategories] = useState({});
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredCategories, setFilteredCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch skills data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        // In a real app, you would fetch categories and their skills
        // For now, we'll use mock data until the API is ready
        const categoriesData = await skillSyncApi.getCategories();
        console.log("Fetched categories data:", categoriesData);
        // Fallback to mock data for development
        const mockData = [
          {
            id: 1,
            name: "Programming Languages",
            skills: [
              { id: 1, name: "JavaScript", endorsements: 42, level: "Advanced" },
              { id: 2, name: "Python", endorsements: 38, level: "Advanced" },
              { id: 3, name: "Java", endorsements: 27, level: "Intermediate" },
              { id: 4, name: "C++", endorsements: 19, level: "Intermediate" },
              { id: 5, name: "TypeScript", endorsements: 31, level: "Advanced" },
            ]
          },
          {
            id: 2,
            name: "Web Development",
            skills: [
              { id: 6, name: "React", endorsements: 45, level: "Expert" },
              { id: 7, name: "Next.js", endorsements: 36, level: "Advanced" },
              { id: 8, name: "Node.js", endorsements: 33, level: "Advanced" },
              { id: 9, name: "HTML/CSS", endorsements: 40, level: "Expert" },
              { id: 10, name: "Django", endorsements: 25, level: "Intermediate" },
            ]
          },
          {
            id: 3,
            name: "Data Science",
            skills: [
              { id: 11, name: "Machine Learning", endorsements: 22, level: "Intermediate" },
              { id: 12, name: "Data Analysis", endorsements: 29, level: "Advanced" },
              { id: 13, name: "SQL", endorsements: 35, level: "Advanced" },
              { id: 14, name: "Pandas", endorsements: 27, level: "Advanced" },
              { id: 15, name: "TensorFlow", endorsements: 18, level: "Intermediate" },
            ]
          },
          {
            id: 4,
            name: "Design",
            skills: [
              { id: 16, name: "UI/UX Design", endorsements: 31, level: "Advanced" },
              { id: 17, name: "Figma", endorsements: 28, level: "Advanced" },
              { id: 18, name: "Adobe Photoshop", endorsements: 24, level: "Intermediate" },
              { id: 19, name: "Responsive Design", endorsements: 33, level: "Advanced" },
              { id: 20, name: "Wireframing", endorsements: 26, level: "Intermediate" },
            ]
          }
        ];
        
        setCategories(mockData);
        setFilteredCategories(mockData);
        // setCategories(categoriesData);
        // setFilteredCategories(categoriesData);
      } catch (err) {
        console.error("Error fetching skills data:", err);
        setError("Failed to load skills. Please try again later.");
        
        // Fallback to mock data for development
        const mockData = [
          {
            id: 1,
            name: "Programming Languages",
            skills: [
              { id: 1, name: "JavaScript", endorsements: 42, level: "Advanced" },
              { id: 2, name: "Python", endorsements: 38, level: "Advanced" },
              { id: 3, name: "Java", endorsements: 27, level: "Intermediate" },
              { id: 4, name: "C++", endorsements: 19, level: "Intermediate" },
              { id: 5, name: "TypeScript", endorsements: 31, level: "Advanced" },
            ]
          },
          {
            id: 2,
            name: "Web Development",
            skills: [
              { id: 6, name: "React", endorsements: 45, level: "Expert" },
              { id: 7, name: "Next.js", endorsements: 36, level: "Advanced" },
              { id: 8, name: "Node.js", endorsements: 33, level: "Advanced" },
              { id: 9, name: "HTML/CSS", endorsements: 40, level: "Expert" },
              { id: 10, name: "Django", endorsements: 25, level: "Intermediate" },
            ]
          },
          {
            id: 3,
            name: "Data Science",
            skills: [
              { id: 11, name: "Machine Learning", endorsements: 22, level: "Intermediate" },
              { id: 12, name: "Data Analysis", endorsements: 29, level: "Advanced" },
              { id: 13, name: "SQL", endorsements: 35, level: "Advanced" },
              { id: 14, name: "Pandas", endorsements: 27, level: "Advanced" },
              { id: 15, name: "TensorFlow", endorsements: 18, level: "Intermediate" },
            ]
          },
          {
            id: 4,
            name: "Design",
            skills: [
              { id: 16, name: "UI/UX Design", endorsements: 31, level: "Advanced" },
              { id: 17, name: "Figma", endorsements: 28, level: "Advanced" },
              { id: 18, name: "Adobe Photoshop", endorsements: 24, level: "Intermediate" },
              { id: 19, name: "Responsive Design", endorsements: 33, level: "Advanced" },
              { id: 20, name: "Wireframing", endorsements: 26, level: "Intermediate" },
            ]
          }
        ];
        
        setCategories(mockData);
        setFilteredCategories(mockData);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Toggle category expansion
  const toggleExpand = (categoryId) => {
    setExpandedCategories(prev => ({
      ...prev,
      [categoryId]: !prev[categoryId]
    }));
  };

  // Handle skill endorsement
  const handleEndorse = async (skillId) => {
    try {
      await skillsApi.endorseSkill(skillId);
      
      // Update the local state to reflect the endorsement
      const updatedCategories = categories.map(category => ({
        ...category,
        skills: category.skills.map(skill => 
          skill.id === skillId 
            ? { ...skill, endorsements: skill.endorsements + 1 }
            : skill
        )
      }));
      
      setCategories(updatedCategories);
      
      // Also update filtered categories if they're being used
      if (searchTerm) {
        setFilteredCategories(prevFiltered => 
          prevFiltered.map(category => ({
            ...category,
            skills: category.skills.map(skill => 
              skill.id === skillId 
                ? { ...skill, endorsements: skill.endorsements + 1 }
                : skill
            )
          }))
        );
      }
    } catch (error) {
      console.error("Error endorsing skill:", error);
      // Show error notification to user
    }
  };

  // Filter skills based on search term
  useEffect(() => {
    if (searchTerm === "") {
      setFilteredCategories(categories);
      return;
    }

    const filtered = categories.map(category => {
      const filteredSkills = category.skills.filter(skill => 
        skill.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      
      return {
        ...category,
        skills: filteredSkills
      };
    }).filter(category => category.skills.length > 0);

    setFilteredCategories(filtered);
  }, [searchTerm, categories]);

  if (isLoading) {
    return <SkillsLoading />;
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl text-center">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p>{error}</p>
          <button 
            className="mt-2 text-red-600 hover:text-red-800 font-medium"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Skills Showcase</h1>
        <p className="text-gray-600">Discover and connect with professionals based on their skills</p>
      </motion.div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Search skills..."
            className="w-full p-3 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <svg 
            className="absolute left-3 top-3.5 h-5 w-5 text-gray-400" 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <div className="flex flex-wrap gap-2 mt-4">
          <button 
            className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-blue-700"
            onClick={() => setSearchTerm("")}
          >
            All Skills
          </button>
          <button 
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-medium hover:bg-gray-300"
            onClick={() => {
              // Sort categories by most endorsed skills
              const sortedCategories = categories.map(category => ({
                ...category,
                skills: [...category.skills].sort((a, b) => b.endorsements - a.endorsements)
              }));
              setFilteredCategories(sortedCategories);
            }}
          >
            Most Endorsed
          </button>
          <button 
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-medium hover:bg-gray-300"
            onClick={() => {
              // In a real app, you would sort by creation date
              // For now, we'll just randomize the order
              const shuffledCategories = categories.map(category => ({
                ...category,
                skills: [...category.skills].sort(() => Math.random() - 0.5)
              }));
              setFilteredCategories(shuffledCategories);
            }}
          >
            Recently Added
          </button>
        </div>
      </div>

      {/* Skills Categories */}
      <div>
        {filteredCategories.length > 0 ? (
          filteredCategories.map(category => (
            <CategorySection 
              key={category.id} 
              category={category} 
              isExpanded={expandedCategories[category.id] || false}
              toggleExpand={toggleExpand}
              onEndorse={handleEndorse}
            />
          ))
        ) : (
          <div className="text-center py-10">
            <p className="text-gray-600 text-lg">No skills found matching your search.</p>
            <button 
              className="mt-4 text-blue-600 hover:text-blue-800 font-medium"
              onClick={() => setSearchTerm("")}
            >
              Clear search
            </button>
          </div>
        )}
      </div>

      {/* Add Skill Button */}
      <motion.div 
        className="fixed bottom-8 right-8"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <Link href="/skills/add">
          <button className="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-6 w-6" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </Link>
      </motion.div>
    </div>
  );
}

// Export the page with Suspense
export default function SkillsPage() {
  return (
    <Suspense fallback={<SkillsLoading />}>
      <SkillsContent />
    </Suspense>
  );
} 