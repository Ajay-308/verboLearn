import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import { auth } from "@clerk/nextjs";

const prisma = new PrismaClient();

export async function POST(req: Request) {
  // Authenticate the user and get the userId
  const { userId } = auth();

  // Parse the JSON body from the request
  const { userMessage, botMessage } = await req.json();

  console.log("User ID:", userId);
  console.log("Inside chat history");

  // Validate input
  if (!userMessage || !botMessage || !userId) {
    return NextResponse.json(
      { error: "User ID, User message, and Bot message are required" },
      { status: 400 },
    );
  }

  try {
    // Check if the user exists in the database
    const userExists = await prisma.user.findUnique({
      where: { externalId: userId },
    });

    if (!userExists) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    console.log("User message:", userMessage);
    console.log("Bot message:", botMessage);

    // Create a new chat message in the database
    const chatMessage = await prisma.chatMessage.create({
      data: {
        userId,
        userMessage: userMessage,
        botMessage: botMessage,
      },
    });

    // Return the saved chat message
    return NextResponse.json(chatMessage, { status: 201 });
  } catch (error) {
    console.error("Error saving chat message:", error);
    return NextResponse.json(
      { error: "Failed to save chat message" },
      { status: 500 },
    );
  }
}
