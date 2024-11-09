"use client";

import { useEffect, useState } from "react";

interface Task {
  incorrect: string;
  correct: string;
  explanation: string;
  options?: string[];
}

interface NotificationProps {
  tasks: Task[];
}

function Notification({ tasks }: NotificationProps) {
  const [showNotification, setShowNotification] = useState(false);

  useEffect(() => {
    if (tasks && tasks.length > 0) {
      setShowNotification(true);
    }
  }, [tasks]);

  return (
    <div className="fixed inset-0 z-50 flex min-h-screen items-center justify-center bg-[#0A0118] p-6 text-white">
      {showNotification && (
        <div
          className="max-w-2xl rounded-lg bg-[#2A1D46] p-8 shadow-lg"
          role="alert"
        >
          <h3 className="mb-4 text-2xl font-semibold">
            New Weekly English Tasks
          </h3>
          <ul className="space-y-6">
            {tasks.map((task, index) => (
              <li key={index} className="text-base">
                <div className="font-medium text-purple-400">Incorrect:</div>
                <p>{task.incorrect}</p>
                <div className="font-medium text-green-400">Correct:</div>
                <p>{task.correct}</p>
                <div className="font-medium text-blue-400">Explanation:</div>
                <p>{task.explanation}</p>
                {task.options && (
                  <div>
                    <div className="font-medium text-yellow-400">Options:</div>
                    <ul className="list-disc pl-4">
                      {task.options.map((option, optionIndex) => (
                        <li key={optionIndex}>{option}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Notification;
