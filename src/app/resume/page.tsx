"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import Navbar from "../home/Navbar";
import Footer from "../home/footer";

interface AnalysisPoint {
  title: string;
  description: string;
}

interface AnalysisResponse {
  summary: string;
  strengths: AnalysisPoint[];
  weaknesses: AnalysisPoint[];
  suggestions: AnalysisPoint[];
}

export default function ResumeAnalyzer() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [customQuery, setCustomQuery] = useState("");
  const [response, setResponse] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeResume = async (queryType: string) => {
    if (!file || !jobDescription) {
      setError("Please upload a PDF file and provide a job description");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);
    formData.append("query_type", queryType);
    if (queryType === "custom") {
      formData.append("custom_query", customQuery);
    }

    try {
      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResponse(data);
      }
    } catch (err) {
      setError("Failed to analyze resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const renderAnalysisSection = (
    title: string,
    points: AnalysisPoint[] | undefined,
  ) => {
    if (!points) return null;

    return (
      <div className="mb-6">
        <h3 className="mb-4 text-xl font-bold text-white">{title}</h3>
        <div className="space-y-4">
          {points.map((point, index) => (
            <div
              key={index}
              className="rounded-lg border border-gray-700 bg-gray-800 p-4"
            >
              <h4 className="mb-2 font-semibold text-blue-400">
                {point.title}
              </h4>
              <p className="text-gray-300">{point.description}</p>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div>
      <Navbar />
      <div className="min-h-full bg-black pt-24">
        <div className="container mx-auto max-w-4xl p-4">
          <Card className="mb-8 bg-gray-900 text-white">
            <CardHeader>
              <CardTitle className="text-white">ATS Resume Analyzer</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Upload Resume (PDF)
                  </label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={(e) => {
                        if (e.target.files && e.target.files.length > 0) {
                          setFile(e.target.files[0]);
                        }
                      }}
                      className="block w-full text-sm text-gray-300
                      file:mr-4 file:rounded-md file:border-0
                      file:bg-gray-700 file:px-4
                      file:py-2 file:text-sm
                      file:font-semibold file:text-gray-300
                      hover:file:bg-gray-600"
                    />
                  </div>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Job Description
                  </label>
                  <Textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    className="h-32 border-gray-700 bg-gray-800 text-white"
                    placeholder="Paste the job description here..."
                  />
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <Button
                    onClick={() => analyzeResume("tell_me_about")}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700"
                  >
                    Tell Me About the Resume
                  </Button>
                  <Button
                    onClick={() => analyzeResume("improve_skills")}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700"
                  >
                    How Can I Improve Skills
                  </Button>
                  <Button
                    onClick={() => analyzeResume("missing_keywords")}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700"
                  >
                    Missing Keywords
                  </Button>
                  <Button
                    onClick={() => analyzeResume("percentage_match")}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700"
                  >
                    Percentage Match
                  </Button>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Custom Query
                  </label>
                  <Textarea
                    value={customQuery}
                    onChange={(e) => setCustomQuery(e.target.value)}
                    className="mb-2 h-20 border-gray-700 bg-gray-800 text-white"
                    placeholder="Ask your own question..."
                  />
                  <Button
                    onClick={() => analyzeResume("custom")}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white hover:bg-blue-700"
                  >
                    Submit Custom Query
                  </Button>
                </div>

                {error && (
                  <div className="rounded-md bg-red-900 p-4 text-red-100">
                    {error}
                  </div>
                )}

                {loading && (
                  <div className="p-4 text-center text-gray-300">
                    <div className="animate-pulse">
                      Processing your request...
                    </div>
                  </div>
                )}

                {response && (
                  <Card className="bg-gray-900 text-white">
                    <CardHeader>
                      <CardTitle className="text-white">
                        Analysis Result
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-6">
                        {/* Summary Section */}
                        <div className="mb-6">
                          <h3 className="mb-4 text-xl font-bold text-white">
                            Summary of Analysis
                          </h3>
                          <p className="rounded-lg border border-gray-700 bg-gray-800 p-4 text-gray-300">
                            {response.summary}
                          </p>
                        </div>

                        {/* Render other sections */}
                        {renderAnalysisSection("Strengths", response.strengths)}
                        {renderAnalysisSection(
                          "Weaknesses",
                          response.weaknesses,
                        )}
                        {renderAnalysisSection(
                          "Suggestions for Improvement",
                          response.suggestions,
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      <div className="-mt-20">
        <Footer />
      </div>
    </div>
  );
}
