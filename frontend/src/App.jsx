import { Routes, Route, Navigate } from "react-router-dom";
//App
import Login from "./pages/Login";
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

      <Route path="/" element={<Login />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/diagnostic" element={<Diagnostic />} />

      <Route path="/results" element={<Results />} />

      <Route path="/learning-path" element={<LearningPath />} />

      <Route path="/lesson/:id" element={<Lesson />} />

      <Route path="/quiz" element={<Quiz />} />

      <Route path="/quiz-result" element={<QuizResult />} />

      <Route path="/progress" element={<Progress />} />

      <Route path="/tutor" element={<Tutor />} />

      <Route
        path="*"
        element={<Navigate to="/dashboard" replace />}
      />

    </Routes>
  );
}

export default App;