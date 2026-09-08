import {
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Login from "./pages/login";
import Onboarding from "./pages/Onboarding";
import LearnerProfile from "./pages/LearnerProfile";

import Dashboard from "./pages/Dashboard";
import Diagnostic from "./pages/Diagnostic";
import Results from "./pages/Results";
import LearningPath from "./pages/LearningPath";
import Lesson from "./pages/Lesson";
import Quiz from "./pages/Quiz";
import QuizResult from "./pages/QuizResult";
import Progress from "./pages/Progress";
import Tutor from "./pages/Tutor";

function App() {

  return (

    <Routes>

      {/* Authentication */}

      <Route
        path="/"
        element={<Login />}
      />


      {/* Personalization */}

      <Route
        path="/onboarding"
        element={<Onboarding />}
      />

      <Route
        path="/learner-profile"
        element={<LearnerProfile />}
      />


      {/* Main Application */}

      <Route
        path="/dashboard"
        element={<Dashboard />}
      />

      <Route
        path="/diagnostic"
        element={<Diagnostic />}
      />

      <Route
        path="/results"
        element={<Results />}
      />

      <Route
        path="/learning-path"
        element={<LearningPath />}
      />

      <Route
        path="/lesson/:id"
        element={<Lesson />}
      />

      <Route
        path="/quiz"
        element={<Quiz />}
      />

      <Route
        path="/quiz-result"
        element={<QuizResult />}
      />

      <Route
        path="/progress"
        element={<Progress />}
      />

      <Route
        path="/tutor"
        element={<Tutor />}
      />


      {/* Fallback */}

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>

  );

}

export default App;