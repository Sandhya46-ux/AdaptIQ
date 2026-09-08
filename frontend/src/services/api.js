// frontend/src/services/api.js

const API_BASE_URL = "http://127.0.0.1:8000";

/* =====================================================
   COMMON API REQUEST
===================================================== */

async function apiRequest(endpoint, options = {}) {
  try {
    const response = await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || data.message || "Something went wrong"
      );
    }

    return data;

  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}


/* =====================================================
   HEALTH CHECK
===================================================== */

export async function checkBackend() {
  return apiRequest("/health");
}


/* =====================================================
   DIAGNOSTIC TEST
===================================================== */

export async function submitDiagnostic(data) {
  return apiRequest("/diagnostic/submit", {
    method: "POST",
    body: JSON.stringify(data),
  });
}


/* =====================================================
   QUIZ
===================================================== */

// Get questions for a concept
export async function getQuizQuestions(
  conceptId,
  difficulty = ""
) {
  let endpoint =
    `/quiz/questions?concept_id=${encodeURIComponent(conceptId)}`;

  if (difficulty) {
    endpoint +=
      `&difficulty=${encodeURIComponent(difficulty)}`;
  }

  return apiRequest(endpoint);
}


// Submit quiz
export async function submitQuiz(data) {
  return apiRequest("/quiz/submit", {
    method: "POST",
    body: JSON.stringify(data),
  });
}


/* =====================================================
   LEARNING PATH
===================================================== */

export async function getLearningPath(studentId) {
  return apiRequest(
    `/learning-path/${encodeURIComponent(studentId)}`
  );
}


/* =====================================================
   PROGRESS
===================================================== */

export async function getProgress(studentId) {
  return apiRequest(
    `/progress/${encodeURIComponent(studentId)}`
  );
}


/* =====================================================
   AI TUTOR
===================================================== */

export async function askTutor(data) {
  return apiRequest("/tutor/ask", {
    method: "POST",
    body: JSON.stringify(data),
  });
}


/* =====================================================
   LOGOUT
===================================================== */

export function logoutUser() {
  localStorage.removeItem("adaptIQUser");
  localStorage.removeItem("adaptIQProfile");
  localStorage.removeItem("adaptIQDiagnostic");
}