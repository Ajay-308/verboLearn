"use client";

import React, { useState } from "react";
import Navbar from "../home/Navbar"; // Assuming you have a Navbar component
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ResumeEvaluation() {
  const [jobDescription, setJobDescription] = useState<string>(""); // State for job description input
  const [resumeFile, setResumeFile] = useState<File | null>(null); // State for resume file upload
  const [task, setTask] = useState<string>("evaluation"); // State for selected task
  const [response, setResponse] = useState<string>(""); // State to hold the response from the API
  const [loading, setLoading] = useState<boolean>(false); // State to show loading indicator

  // List of tasks
  const taskOptions = [
    { value: "evaluation", label: "Resume Evaluation" },
    { value: "improvement", label: "Resume Improvement" },
    { value: "keywords", label: "ATS Keywords" },
    { value: "percentage_match", label: "Percentage Match" },
  ];

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); // Show loader while processing request

    if (!resumeFile || !jobDescription) {
      alert("Please fill in all fields.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", resumeFile); // Append resume file
    formData.append("job_description", jobDescription); // Append job description
    formData.append("task", task); // Append task

    try {
      const response = await fetch("http://localhost:8000/process", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data.response); // Set response from the API
      } else {
        console.error("Failed to process resume", response.statusText);
        alert("Failed to process the resume. Please try again.");
      }
    } catch (error) {
      console.error("Error during resume evaluation:", error);
    } finally {
      setLoading(false); // Hide loader after request completion
    }
  };

  return (
    <div className="h-screen bg-black text-white">
      <Navbar />
      <div className="container mx-auto p-4">
        <h1 className="mb-4 text-2xl font-bold">Resume Evaluation</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="jobDescription" className="mb-1 block text-white">
              Job Description:
            </label>
            <input
              type="text"
              id="jobDescription"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full rounded-md border bg-gray-800 px-3 py-2"
              required
            />
          </div>

          <div>
            <label htmlFor="resumeFile" className="mb-1 block text-white">
              Upload Resume (PDF):
            </label>
            <Input
              type="file"
              id="resumeFile"
              onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              className="rounded-md border bg-gray-800 text-white"
              accept=".pdf"
              required
            />
          </div>

          <div>
            <label htmlFor="task" className="mb-1 block text-white">
              Select Task:
            </label>
            <select
              id="task"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              className="w-full rounded-md border bg-gray-800 px-3 py-2"
              required
            >
              {taskOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <Button
            type="submit"
            className="rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
          >
            Submit
          </Button>
        </form>

        {loading && <div className="mt-4 text-center">Loading...</div>}

        <div id="result" className="mt-8">
          {response && (
            <>
              <h2 className="font-bold">Result:</h2>
              <p>{response}</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
