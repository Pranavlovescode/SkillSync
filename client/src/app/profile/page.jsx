'use client'
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { FiEdit, FiLogOut, FiSettings } from "react-icons/fi";
import { authApi, skillSyncApi } from "@/lib/api";
import toast from "react-hot-toast";


export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    title: "",
    bio: "",
    skills: [],
  });

  // Fetch user data
  useEffect(() => {
    // Replace with actual API call to get user data
    const fetchUserData = async () => {
      try {
        // Mock data - replace with actual API call
        const userData = {
          id: "123",
          name: "Alex Johnson",
          email: "alex@example.com",
          avatar: "https://randomuser.me/api/portraits/men/32.jpg",
          title: "Full Stack Developer",
          bio: "Passionate developer with 5+ years of experience in web and mobile application development.",
          skills: ["React", "Node.js", "JavaScript", "TypeScript", "MongoDB"],
          projects: [
            {
              id: 1,
              name: "E-commerce Platform",
              description: "Built a full-stack e-commerce solution",
            },
            {
              id: 2,
              name: "Task Management App",
              description: "Developed a collaborative task tracker",
            },
          ],
        };

        setUser(userData);
        setFormData({
          name: userData.name,
          title: userData.title,
          bio: userData.bio,
          skills: userData.skills,
        });
        setLoading(false);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleEditToggle = () => {
    setEditMode(!editMode);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSkillChange = (e) => {
    const skillsArray = e.target.value.split(",").map((skill) => skill.trim());
    setFormData((prev) => ({
      ...prev,
      skills: skillsArray,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Replace with actual API call to update user profile
    try {
      // Mock update - replace with actual API call
      setUser((prev) => ({
        ...prev,
        name: formData.name,
        title: formData.title,
        bio: formData.bio,
        skills: formData.skills,
      }));

      setEditMode(false);
      // Show success message
    } catch (error) {
      console.error("Error updating profile:", error);
      // Show error message
    }
  };

  const handleLogout = async() => {
    // Replace with actual logout logic
    const response = await authApi.logout();
    if (response.status === 200){
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      // Show success message
      toast.success("Logged out successfully!");
      router.push("/");
    }
    else{
      // Show error message
      toast.error("Error logging out. Please try again.");
      console.error("Logout error:", response);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
          <div className="flex space-x-4">
            <button
              onClick={handleEditToggle}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
            >
              <FiEdit className="mr-2" /> {editMode ? "Cancel" : "Edit Profile"}
            </button>
            <button
              onClick={() => router.push("/settings")}
              className="flex items-center px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
            >
              <FiSettings className="mr-2" /> Settings
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
            >
              <FiLogOut className="mr-2" /> Logout
            </button>
          </div>
        </div>

        {/* Profile Content */}
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-32 sm:h-48"></div>
          <div className="px-4 py-5 sm:p-6 -mt-16 sm:-mt-24">
            <div className="flex flex-col sm:flex-row items-center">
              <div className="relative">
                <Image
                  src={user.avatar || "https://via.placeholder.com/150"}
                  alt={user.name}
                  width={120}
                  height={120}
                  className="rounded-full border-4 border-white shadow-md"
                  priority
                />
                {!editMode && (
                  <div className="absolute bottom-0 right-0 bg-blue-500 p-2 rounded-full text-white">
                    <FiEdit size={16} />
                  </div>
                )}
              </div>

              <div className="mt-4 sm:mt-0 sm:ml-6 text-center sm:text-left">
                <h2 className="text-2xl font-bold text-gray-900">
                  {user.name}
                </h2>
                <p className="text-gray-600">{user.title}</p>
                <p className="mt-1 text-sm text-gray-500">{user.email}</p>
              </div>
            </div>

            {editMode ? (
              <form onSubmit={handleSubmit} className="mt-6">
                <div className="space-y-4">
                  <div>
                    <label
                      htmlFor="name"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Name
                    </label>
                    <input
                      type="text"
                      name="name"
                      id="name"
                      value={formData.name}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="title"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Professional Title
                    </label>
                    <input
                      type="text"
                      name="title"
                      id="title"
                      value={formData.title}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="bio"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Bio
                    </label>
                    <textarea
                      name="bio"
                      id="bio"
                      rows={4}
                      value={formData.bio}
                      onChange={handleChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="skills"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Skills (comma separated)
                    </label>
                    <input
                      type="text"
                      name="skills"
                      id="skills"
                      value={formData.skills.join(", ")}
                      onChange={handleSkillChange}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
                    >
                      Save Changes
                    </button>
                  </div>
                </div>
              </form>
            ) : (
              <div className="mt-6">
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900">About</h3>
                  <p className="mt-2 text-gray-600">{user.bio}</p>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900">Skills</h3>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {user.skills.map((skill, index) => (
                      <span
                        key={index}
                        className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {user.projects && user.projects.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-medium text-gray-900">
                      Projects
                    </h3>
                    <div className="mt-2 space-y-3">
                      {user.projects.map((project) => (
                        <div
                          key={project.id}
                          className="bg-gray-50 p-4 rounded-md"
                        >
                          <h4 className="font-medium">{project.name}</h4>
                          <p className="text-sm text-gray-600">
                            {project.description}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Additional sections can be added below */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Recent Activity
            </h3>
            <div className="space-y-3">
              <p className="text-sm text-gray-500">No recent activity</p>
              {/* Add activity items here */}
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Connections
            </h3>
            <div className="space-y-3">
              <p className="text-sm text-gray-500">No connections yet</p>
              {/* Add connections here */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
