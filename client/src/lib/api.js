import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // Important for cookies/session
});

// Add request interceptor to include auth token
// api.interceptors.request.use(
//   (config) => {
//     // Get token from localStorage if available
//     const token =
//       typeof window !== "undefined" ? localStorage.getItem("token") : null;

//     if (token) {
//       config.headers["Authorization"] = `Token ${token}`;
//     }

//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// Skills API endpoints
export const skillSyncApi = {

  // login API
  loginApi: async (credentials) => {
    try {
      const response = await api.post("/api/login/", credentials);
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
      }
      return response;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },


  // Get all skills
  getAllSkills: async () => {
    try {
      const response = await api.get("/api/skills/");
      return response.data;
    } catch (error) {
      console.error("Error fetching skills:", error);
      throw error;
    }
  },

  // Get skills by category
  getSkillsByCategory: async (categoryId) => {
    try {
      const response = await api.get(`/api/skills/category/${categoryId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching skills for category ${categoryId}:`, error);
      throw error;
    }
  },

  // Add a new skill
  addSkill: async (skillData) => {
    try {
      const response = await api.post("/skill/post/", skillData);
      return response.data;
    } catch (error) {
      console.error("Error adding skill:", error);
      throw error;
    }
  },

  // Endorse a skill
  endorseSkill: async (skillId) => {
    try {
      const response = await api.post(`/api/skills/${skillId}/endorse/`);
      return response.data;
    } catch (error) {
      console.error(`Error endorsing skill ${skillId}:`, error);
      throw error;
    }
  },

  // Get skill categories
  getCategories: async () => {
    try {
      const response = await api.get("/skill/skills-category/",{
        withCredentials:true,
        headers:{
          'Content-Type':'application/json',
        }
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching skill categories:", error);
      throw error;
    }
  },
};

// Auth API endpoints
export const authApi = {
  login: async (credentials) => {
    try {
      const response = await api.post("/api/login/", credentials);
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
      }
      return response.data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },

  logout: async () => {
    try {
      const response = await api.post("/api/logout/");
      localStorage.removeItem("token");
      return response.data;
    } catch (error) {
      console.error("Logout error:", error);
      // Still remove token even if API call fails
      localStorage.removeItem("token");
      throw error;
    }
  },
};

export default api;
