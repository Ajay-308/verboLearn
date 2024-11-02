import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import { auth } from "@clerk/nextjs";

const prisma = new PrismaClient();

console.log("hi i am inside database");
export async function POST(req: Request) {
  console.log("inside post");
  const { userId } = auth();
  const { userMessage, botMessage } = await req.json();

  if (!userMessage || !botMessage || !userId) {
    return NextResponse.json(
      { error: "User ID, User message, and Bot message are required" },
      { status: 400 },
    );
  }

  try {
    const userExists = await prisma.user.findUnique({
      where: { externalId: userId },
    });

    if (!userExists) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    // Ensure botMessage is a string
    const botMessageString = Array.isArray(botMessage)
      ? botMessage.join(" ")
      : botMessage;

    const chatMessage = await prisma.learnMessage.create({
      data: {
        userId,
        userMessage,
        botMessage: botMessageString,
      },
    });

    return NextResponse.json(chatMessage, { status: 201 });
  } catch (error) {
    console.error("Error saving chat message:", error);
    return NextResponse.json(
      { error: "Failed to save chat message" },
      { status: 500 },
    );
  }
}

export async function GET(req: Request) {
  const { userId } = auth();

  try {
    const chatMessages = await prisma.learnMessage.findMany({
      where: {
        userId: userId ?? undefined,
      },
      include: {
        user: true,
      },
      orderBy: {
        createdAt: "desc",
      },
    });

    return NextResponse.json(chatMessages, { status: 200 });
  } catch (error) {
    console.error("Error fetching chat messages:", error);
    return NextResponse.json(
      { error: "Failed to fetch chat messages" },
      { status: 500 },
    );
  }
}
