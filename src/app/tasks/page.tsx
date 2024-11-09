"use client";
import { useState, useEffect } from "react";
import Notification from "../../components/notification";
import Navbar from "../home/Navbar";
import Footer from "../home/footer";

export default function NotificationsPage() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Fetch tasks every Tuesday
    const fetchTasks = async () => {
      try {
        const response = await fetch("http://localhost:8000/generate-tasks");
        const data = await response.json();
        setTasks(data.tasks);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    // Check if today is Tuesday
    // const today = new Date();
    // if (today.getDay() === 2) {
    //   fetchTasks();
    // }
    fetchTasks();
  }, []);

  return (
    <>
      <Navbar />
      <div>
        <Notification tasks={tasks} />
      </div>
    </>
  );
}
